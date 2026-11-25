import json
from pathlib import Path
import sys
import os

# Use the same Python interpreter for Spark Driver and Workers
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

import query_processing as qp
import similarity as sim
import tfidf as tfidf_mod


ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"
DEFAULT_DATASET = ROOT / "dataset"

sys.path.insert(0, str(ROOT / "src"))


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_default_dataset():
    full_output_path = OUTPUTS / "full_output.json"

    if not full_output_path.exists():
        raise FileNotFoundError(
            "Default dataset outputs were not found."
        )

    data = load_json(full_output_path)

    return {
        "dataset_name": DEFAULT_DATASET.name,
        "document_count": len(data["document_vector_lengths"]),
        "positional_index": data["positional_index"],
        "tf": data["term_frequency"],
        "weighted_tf": data["weighted_tf"],
        "df": data["document_frequency"],
        "idf": data["idf"],
        "tfidf": data["tfidf"],
        "doc_lengths": data["document_vector_lengths"],
        "normalized_tfidf": data["normalized_tfidf"],
        "phrase_queries": data["phrase_queries"],
        "boolean_queries": data["boolean_queries"],
    }


def build_document_vectors(normalized_tfidf):
    return tfidf_mod.get_document_vectors(normalized_tfidf)


def search_dataset(data, query, query_type):
    index = data["positional_index"]
    idf = data["idf"]

    doc_vectors = build_document_vectors(
        data["normalized_tfidf"]
    )

    if query_type == "Phrase Query":
        matches = qp.phrase_query(index, query)

        matching_docs = sorted(
            {match["document"] for match in matches},
            key=sim.doc_sort_key
        )

    elif query_type == "Boolean Query":
        matching_docs = qp.boolean_search(index, query)
        matches = []

    else:
        raise ValueError("Invalid query type.")

    similarity_result = sim.evaluate_query(
        query,
        matching_docs,
        idf,
        doc_vectors
    )

    return {
        "query": query,
        "query_type": query_type,
        "matching_documents": matching_docs,
        "matches": matches,
        "similarity": similarity_result,
    }


def build_dataset(dataset_path, output_dir=None):
    from pyspark.sql import SparkSession
    import positional_index as pi
    import term_statistics as ts

    dataset_path = Path(dataset_path).resolve()

    if not dataset_path.is_dir():
        raise FileNotFoundError(
            f"Dataset folder not found: {dataset_path}"
        )

    if output_dir is None:
        output_dir = (
            OUTPUTS / "generated" / dataset_path.name
        )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create Spark Session
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("IR_Streamlit_Index_Builder")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    try:
        # 1. Build Positional Index using PySpark
        index = pi.build_positional_index(
            spark,
            dataset_path
        )

    finally:
        spark.stop()

    # 2. Calculate Term Statistics
    tf, weighted_tf, df, idf = ts.compute_all(index)

    # 3. Calculate TF-IDF and Normalization
    statistics = {
        "tf": tf,
        "weighted_tf": weighted_tf,
        "df": df,
        "idf": idf,
    }

    tfidf, doc_lengths, normalized = (
        tfidf_mod.compute_all(statistics)
    )

    # 4. Prepare all results
    data = {
        "dataset_name": dataset_path.name,
        "document_count": len(doc_lengths),
        "positional_index": index,
        "tf": tf,
        "weighted_tf": weighted_tf,
        "df": df,
        "idf": idf,
        "tfidf": tfidf,
        "doc_lengths": doc_lengths,
        "normalized_tfidf": normalized,
        "phrase_queries": [],
        "boolean_queries": [],
    }

    # 5. Save outputs separately
    pi.save_positional_index(
        index,
        output_dir / "positional_index.json"
    )

    with open(
        output_dir / "term_statistics.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(statistics, file, indent=4)

    tfidf_output = {
        "tfidf": tfidf,
        "doc_lengths": doc_lengths,
        "normalized_tfidf": normalized,
    }

    with open(
        output_dir / "tfidf.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(tfidf_output, file, indent=4)

    full_output = {
        "positional_index": index,
        "term_frequency": tf,
        "weighted_tf": weighted_tf,
        "document_frequency": df,
        "idf": idf,
        "tfidf": tfidf,
        "document_vector_lengths": doc_lengths,
        "normalized_tfidf": normalized,
        "phrase_queries": [],
        "boolean_queries": [],
    }

    with open(
        output_dir / "full_output.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(full_output, file, indent=4)

    return data
