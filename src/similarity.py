import math


def doc_sort_key(doc_id):
    number = doc_id[1:]
    return int(number) if number.isdigit() else doc_id


def extract_query_terms(query, include_negated=False):
    tokens = query.replace("(", " ").replace(")", " ").split()
    terms = []
    negated = False
    for token in tokens:
        upper = token.upper()
        if upper == "NOT":
            negated = True
        elif upper in ("AND", "OR"):
            negated = False
        elif include_negated or not negated:
            terms.append(token.lower())
    return terms


def build_query_vector(terms, idf):
    counts = {}
    for term in terms:
        if term in idf:
            counts[term] = counts.get(term, 0) + 1

    weighted = {t: 1 + math.log10(c) for t, c in counts.items()}
    tfidf = {t: weighted[t] * idf[t] for t in counts}

    length = math.sqrt(sum(w ** 2 for w in tfidf.values()))
    normalized = {t: (w / length if length > 0 else 0.0) for t, w in tfidf.items()}

    details = [
        {"term": t, "weighted_tf": weighted[t], "tfidf": tfidf[t], "normalized": normalized[t]}
        for t in counts
    ]
    return details, normalized, length


def cosine_similarity(query_vector, doc_vector):
    return sum(w * doc_vector.get(t, 0.0) for t, w in query_vector.items())


def score_documents(doc_ids, query_vector, doc_vectors):
    return {
        doc: cosine_similarity(query_vector, doc_vectors[doc])
        for doc in sorted(doc_ids, key=doc_sort_key)
    }


def rank_documents(scores):
    return sorted(scores.items(), key=lambda item: (-round(item[1], 10), doc_sort_key(item[0])))


def evaluate_query(query, matching_docs, idf, doc_vectors):
    terms = extract_query_terms(query)
    details, q_vector, q_length = build_query_vector(terms, idf)
    scores = score_documents(matching_docs, q_vector, doc_vectors)
    return {
        "query": query,
        "query_terms": details,
        "query_length": q_length,
        "scores": scores,
        "ranking": rank_documents(scores),
    }


def print_similarity_report(title, result):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)
    print(f"Query vector length = {result['query_length']:.6f}")
    print("{:<14}{:>12}{:>14}{:>18}".format("Query term", "Weighted TF", "Query TF-IDF", "Normalized weight"))
    for item in result["query_terms"]:
        print("{:<14}{:>12.4f}{:>14.4f}{:>18.4f}".format(
            item["term"], item["weighted_tf"], item["tfidf"], item["normalized"]))

    print("\n{:<18}{:>12}".format("Matched document", "Similarity"))
    if not result["scores"]:
        print("(no matching documents)")
    for doc, score in result["scores"].items():
        print("{:<18}{:>12.4f}".format(doc, score))

    if result["ranking"]:
        print("\nRanking (highest similarity first):", " > ".join(d for d, _ in result["ranking"]))
    else:
        print("\nRanking: (empty)")