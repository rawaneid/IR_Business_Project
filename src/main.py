import argparse
import json
from pathlib import Path

import query_processing as qp
import similarity as sim
import term_statistics as ts
import tfidf as tfidf_mod

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"

PHRASE_QUERIES = ["customer service", "sales growth"]
BOOLEAN_QUERIES = [
    "customer service AND sales growth",
    "customer service AND NOT sales growth",
]


def banner(text):
    print("\n" + "#" * 64)
    print("# " + text)
    print("#" * 64)


def get_positional_index(skip_spark):
    index_path = OUTPUTS / "positional_index.json"

    if not skip_spark:
        try:
            from pyspark.sql import SparkSession
            import positional_index as pi
        except ImportError:
            print("[!] PySpark is not installed -> using the saved index instead.")
        else:
            spark = (SparkSession.builder.master("local[2]")
                     .appName("Business_Positional_Index").getOrCreate())
            spark.sparkContext.setLogLevel("ERROR")
            try:
                index = pi.build_positional_index(spark, ROOT / "dataset")
                pi.save_positional_index(index, index_path)
                print("Positional index built with Spark and saved to", index_path)
                return index
            finally:
                spark.stop()

    with open(index_path, "r", encoding="utf-8") as file:
        index = json.load(file)
    print("Positional index loaded from", index_path)
    return index


def print_positional_index(index):
    for term, docs in index.items():
        postings = "; ".join(f"{doc}: {', '.join(map(str, pos))}" for doc, pos in docs.items())
        print(f"{term:<14}{postings}")


def print_phrase_matches(query, matches):
    print(f"\nPhrase query: \"{query}\"")
    print("{:<18}{:>20}{:>24}".format("Matched document", "Starting positions", "Phrase token ranges"))
    per_doc = {}
    for m in matches:
        per_doc.setdefault(m["document"], []).append(m)
    for doc, items in per_doc.items():
        starts = ", ".join(str(i["starting_position"]) for i in items)
        ranges = ", ".join(i["phrase_token_range"] for i in items)
        print("{:<18}{:>20}{:>24}".format(doc, starts, ranges))
    if not per_doc:
        print("(no matching documents)")


def run_phrase(index, idf, doc_vectors, query):
    matches = qp.phrase_query(index, query)
    print_phrase_matches(query, matches)
    docs = {m["document"] for m in matches}
    result = sim.evaluate_query(query, docs, idf, doc_vectors)
    result["matches"] = group_matches(matches)
    sim.print_similarity_report(f"Similarity for phrase query: \"{query}\"", result)
    return result


def run_boolean(index, idf, doc_vectors, query):
    docs = qp.boolean_search(index, query)
    print(f"\nBoolean query: \"{query}\"")
    print("Matching documents:", ", ".join(docs) if docs else "(none)")
    result = sim.evaluate_query(query, docs, idf, doc_vectors)
    result["matching_documents"] = list(docs)
    sim.print_similarity_report(f"Similarity for Boolean query: \"{query}\"", result)
    return result


def is_boolean(query):
    return any(tok.upper() in ("AND", "OR", "NOT") for tok in query.split())


def group_matches(matches):
    grouped = {}
    for m in matches:
        entry = grouped.setdefault(
            m["document"], {"document": m["document"], "starting_positions": [], "token_ranges": []})
        entry["starting_positions"].append(m["starting_position"])
        entry["token_ranges"].append(m["phrase_token_range"])
    return list(grouped.values())


def to_json_result(result):
    out = {"query": result["query"]}
    if "matches" in result:
        out["matching_documents"] = [m["document"] for m in result["matches"]]
        out["matches"] = result["matches"]
    else:
        out["matching_documents"] = result["matching_documents"]
    out["similarity"] = {
        "query_vector_length": result["query_length"],
        "query_terms": result["query_terms"],
        "scores": result["scores"],
        "ranking": [doc for doc, _ in result["ranking"]],
    }
    return out


def interactive_loop(index, idf, doc_vectors):
    banner("INTERACTIVE MODE")
    print("Type a phrase query or a Boolean query. Empty line to quit.")
    while True:
        try:
            query = input("\nquery> ").strip()
        except EOFError:
            break
        if not query:
            break
        try:
            if is_boolean(query):
                run_boolean(index, idf, doc_vectors, query)
            else:
                run_phrase(index, idf, doc_vectors, query)
        except ValueError as error:
            print("Invalid query:", error)


def run_pipeline(skip_spark, interactive):
    banner("STEP 1: POSITIONAL INDEX (Spark)")
    index = get_positional_index(skip_spark)
    print()
    print_positional_index(index)

    banner("STEP 2: TF, DF, IDF")
    tf, w_tf, df, idf = ts.compute_all(index)
    ts.print_matrix("RAW TF", tf)
    ts.print_matrix("WEIGHTED TF  (1 + log10 TF)", w_tf)
    ts.print_df_idf(df, idf)
    with open(OUTPUTS / "term_statistics.json", "w") as file:
        json.dump({"tf": tf, "weighted_tf": w_tf, "df": df, "idf": idf}, file, indent=4)

    banner("STEP 3: TF-IDF AND NORMALIZATION")
    tfidf, lengths, normalized = tfidf_mod.compute_all({"weighted_tf": w_tf, "idf": idf})
    tfidf_mod.print_matrix("TF-IDF", tfidf)
    tfidf_mod.print_doc_lengths(lengths)
    tfidf_mod.print_matrix("NORMALIZED TF-IDF", normalized)
    tfidf_mod.save_tfidf(OUTPUTS / "tfidf.json", tfidf, lengths, normalized)
    doc_vectors = tfidf_mod.get_document_vectors(normalized)

    banner("STEP 4: PHRASE QUERIES + SIMILARITY + RANKING")
    phrase_results, boolean_results = [], []
    for query in PHRASE_QUERIES:
        phrase_results.append(to_json_result(run_phrase(index, idf, doc_vectors, query)))

    banner("STEP 5: BOOLEAN QUERIES + SIMILARITY + RANKING")
    for query in BOOLEAN_QUERIES:
        boolean_results.append(to_json_result(run_boolean(index, idf, doc_vectors, query)))

    full_output = {
        "positional_index": index,
        "term_frequency": tf,
        "weighted_tf": w_tf,
        "document_frequency": df,
        "idf": idf,
        "tfidf": tfidf,
        "document_vector_lengths": lengths,
        "normalized_tfidf": normalized,
        "phrase_queries": phrase_results,
        "boolean_queries": boolean_results,
    }
    output_path = OUTPUTS / "full_output.json"
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(full_output, file, indent=4, ensure_ascii=False)
    print("\nFull output saved to", output_path)

    if interactive:
        interactive_loop(index, idf, doc_vectors)


def main():
    parser = argparse.ArgumentParser(description="Business IR system")
    parser.add_argument("--skip-spark", action="store_true",
                        help="reuse outputs/positional_index.json instead of running Spark")
    parser.add_argument("--interactive", action="store_true",
                        help="accept queries typed by the user after the assigned ones")
    args = parser.parse_args()

    OUTPUTS.mkdir(exist_ok=True)
    run_pipeline(args.skip_spark, args.interactive)


if __name__ == "__main__":
    main()