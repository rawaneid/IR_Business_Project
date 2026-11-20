import json
import math
from pathlib import Path


def load_index(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_document_ids(index):
    document_ids = {
        doc
        for term in index
        for doc in index[term]
    }
    return sorted(
        document_ids,
        key=lambda doc: (
            0, int(doc[1:])
        ) if doc.startswith("d") and doc[1:].isdigit()
        else (1, doc.lower())
    )


def compute_tf(index):
    tf = {}
    for term in index:
        tf[term] = {}
        for doc in index[term]:
            tf[term][doc] = len(index[term][doc])
    return tf


def compute_weighted_tf(tf):
    w_tf = {}
    for term in tf:
        w_tf[term] = {}
        for doc in tf[term]:
            w_tf[term][doc] = 1 + math.log10(tf[term][doc])
    return w_tf


def compute_df(index):
    df = {}
    for term in index:
        df[term] = len(index[term])
    return df


def compute_idf(df, document_count):
    idf = {}
    for term in df:
        idf[term] = math.log10(document_count / df[term])
    return idf


def print_matrix(title, matrix, document_ids):
    print("\n" + title)

    print(
        "{:<14}".format("term")
        + "".join("{:>12}".format(doc) for doc in document_ids)
    )

    for term in sorted(matrix):
        row = "{:<14}".format(term)

        for doc in document_ids:
            value = matrix[term].get(doc, 0)
            row += "{:>12.4f}".format(value)

        print(row)


def print_df_idf(df, idf):
    print("\nDF and IDF")
    print("{:<14}{:>5}{:>10}".format("term", "DF", "IDF"))
    for term in sorted(df):
        print(
            "{:<14}{:>5}{:>10.4f}".format(
                term, df[term], idf[term]
            )
        )


def compute_all(index):
    document_ids = get_document_ids(index)
    document_count = len(document_ids)

    if document_count == 0:
        raise ValueError("The positional index contains no documents.")

    tf = compute_tf(index)
    w_tf = compute_weighted_tf(tf)
    df = compute_df(index)
    idf = compute_idf(df, document_count)

    return tf, w_tf, df, idf


def main():
    root = Path(__file__).resolve().parent.parent

    index = load_index(
        root / "outputs" / "positional_index.json"
    )

    tf, w_tf, df, idf = compute_all(index)
    document_ids = get_document_ids(index)

    print(f"\nNumber of documents: {len(document_ids)}")

    print_matrix("RAW TF", tf, document_ids)
    print_matrix("WEIGHTED TF", w_tf, document_ids)
    print_df_idf(df, idf)

    with open(
        root / "outputs" / "term_statistics.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            {
                "tf": tf,
                "weighted_tf": w_tf,
                "df": df,
                "idf": idf
            },
            file,
            indent=4
        )


if __name__ == "__main__":
    main()