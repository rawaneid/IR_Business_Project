import json
import math
from pathlib import Path

DOC_IDS = ["d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10"]
N = 10


def load_index(path):
    with open(path, "r") as file:
        return json.load(file)


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


def compute_idf(df):
    idf = {}
    for term in df:
        idf[term] = math.log10(N / df[term])
    return idf
def print_matrix(title, matrix):
    print("\n" + title)
    print("{:<14}".format("term") + "".join("{:>9}".format(d) for d in DOC_IDS))
    for term in sorted(matrix):
        row = "{:<14}".format(term)
        for doc in DOC_IDS:
            value = matrix[term].get(doc, 0)
            row += "{:>9.4f}".format(value)
        print(row)


def print_df_idf(df, idf):
    print("\nDF and IDF")
    print("{:<14}{:>5}{:>10}".format("term", "DF", "IDF"))
    for term in sorted(df):
        print("{:<14}{:>5}{:>10.4f}".format(term, df[term], idf[term]))


def compute_all(index):
    tf = compute_tf(index)
    w_tf = compute_weighted_tf(tf)
    df = compute_df(index)
    idf = compute_idf(df)
    return tf, w_tf, df, idf


def main():
    root = Path(__file__).resolve().parent.parent
    index = load_index(root / "outputs" / "positional_index.json")

    tf, w_tf, df, idf = compute_all(index)

    print_matrix("RAW TF", tf)
    print_matrix("WEIGHTED TF", w_tf)
    print_df_idf(df, idf)

    with open(root / "outputs" / "term_statistics.json", "w") as file:
        json.dump({"tf": tf, "weighted_tf": w_tf, "df": df, "idf": idf}, file, indent=4)


if __name__ == "__main__":
    main()