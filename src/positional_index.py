from pyspark.sql import SparkSession
from pathlib import Path
import json
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable



def build_positional_index(spark, dataset_path):
    dataset_path = Path(dataset_path).resolve()

    if not dataset_path.is_dir():
        raise FileNotFoundError(
            f"Dataset folder not found: {dataset_path}"
        )

    document_files = sorted(dataset_path.glob("*.txt"))

    if not document_files:
        raise ValueError(
            f"No TXT files found in: {dataset_path}"
        )

    document_data = [
        (str(file_path), file_path.read_text(encoding="utf-8"))
        for file_path in document_files
    ]

    empty_documents = [
        Path(file_path).name
        for file_path, content in document_data
        if not content.split()
    ]

    if empty_documents:
        raise ValueError(
            f"Empty documents found: {', '.join(empty_documents)}"
        )

    documents = spark.sparkContext.parallelize(
        document_data,
        2
    ).cache()

    def extract_positions(document):
        file_path, content = document

        doc_id = Path(file_path).stem
        words = content.lower().split()

        return [
            (word, (doc_id, position))
            for position, word in enumerate(words, start=1)
        ]

    positional_rdd = (
        documents
        .flatMap(extract_positions)
        .groupByKey()
    )

    positional_index = {}

    def document_sort_key(doc_id):
        number = doc_id[1:]

        if doc_id.startswith("d") and number.isdigit():
            return (0, int(number))

        return (1, doc_id.lower())

    for term, entries in positional_rdd.collect():

        sorted_entries = sorted(
            entries,
            key=lambda item: (
                document_sort_key(item[0]),
                item[1]
            )
        )

        positional_index[term] = {}

        for doc_id, position in sorted_entries:
            positional_index[term].setdefault(
                doc_id, []
            ).append(position)

    documents.unpersist()

    return dict(sorted(positional_index.items()))


def save_positional_index(positional_index, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            positional_index,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():
    project_root = Path(__file__).resolve().parent.parent

    dataset_path = project_root / "dataset"
    output_path = project_root / "outputs" / "positional_index.json"

    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("Business_Positional_Index")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    try:
        positional_index = build_positional_index(
            spark, dataset_path
        )

        print("\n========== POSITIONAL INDEX ==========\n")

        for term, documents in positional_index.items():
            print(f"{term}:")

            for doc_id, positions in documents.items():
                print(f"    {doc_id}: {positions}")

        save_positional_index(
            positional_index, output_path
        )

        print("\nPositional Index saved successfully!")
        print(f"Output file: {output_path}")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
