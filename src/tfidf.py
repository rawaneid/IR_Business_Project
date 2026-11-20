import json
import math
from pathlib import Path


def load_statistics(path):
    """Load the output of term_statistics.py (tf, weighted_tf, df, idf)."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_document_ids(matrix):
    document_ids = {
        doc
        for term in matrix
        for doc in matrix[term]
    }

    return sorted(
        document_ids,
        key=lambda doc: (
            0, int(doc[1:])
        ) if doc.startswith("d") and doc[1:].isdigit()
        else (1, doc.lower())
    )


def compute_tfidf(weighted_tf, idf):
    """tf-idf(t, d) = weighted_tf(t, d) * idf(t)."""
    tfidf = {}
    for term in weighted_tf:
        tfidf[term] = {}
        for doc in weighted_tf[term]:
            tfidf[term][doc] = weighted_tf[term][doc] * idf[term]
    return tfidf


def compute_doc_lengths(tfidf):
    """Euclidean length of each document vector: sqrt(sum(w^2))."""
    document_ids = get_document_ids(tfidf)
    sums = {doc: 0.0 for doc in document_ids}

    for term in tfidf:
        for doc, weight in tfidf[term].items():
            sums[doc] += weight ** 2

    return {
        doc: math.sqrt(total)
        for doc, total in sums.items()
    }


def normalize_tfidf(tfidf, doc_lengths):
    """Normalized weight = tf-idf / document length (unit vectors)."""
    normalized = {}
    for term in tfidf:
        normalized[term] = {}
        for doc, weight in tfidf[term].items():
            length = doc_lengths[doc]
            normalized[term][doc] = weight / length if length > 0 else 0.0
    return normalized


def compute_all(stats):
    tfidf = compute_tfidf(
        stats["weighted_tf"],
        stats["idf"]
    )

    doc_lengths = compute_doc_lengths(tfidf)
    normalized = normalize_tfidf(tfidf, doc_lengths)
    return tfidf, doc_lengths, normalized


def get_document_vectors(normalized):
    """Convert {term: {doc: w}} to {doc: {term: w}}."""
    document_ids = get_document_ids(normalized)
    vectors = {doc: {} for doc in document_ids}

    for term in normalized:
        for doc, weight in normalized[term].items():
            vectors[doc][term] = weight
    return vectors


def print_matrix(title, matrix):
    document_ids = get_document_ids(matrix)

    print("\n" + title)
    print(
        "{:<14}".format("term")
        + "".join("{:>12}".format(doc) for doc in document_ids)
    )

    for term in sorted(matrix):
        row = "{:<14}".format(term)

        for doc in document_ids:
            row += "{:>12.4f}".format(matrix[term].get(doc, 0))

        print(row)


def print_doc_lengths(doc_lengths):
    document_ids = sorted(
        doc_lengths,
        key=lambda doc: (
            0, int(doc[1:])
        ) if doc.startswith("d") and doc[1:].isdigit()
        else (1, doc.lower())
    )

    print("\nDOCUMENT LENGTHS")
    print("{:<14}{:>12}".format("doc", "length"))

    for doc in document_ids:
        print("{:<14}{:>12.4f}".format(doc, doc_lengths[doc]))


def save_tfidf(path, tfidf, doc_lengths, normalized):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            {
                "tfidf": tfidf,
                "doc_lengths": doc_lengths,
                "normalized_tfidf": normalized,
            },
            file,
            indent=4,
        )


def main():
    root = Path(__file__).resolve().parent.parent
    stats = load_statistics(
        root / "outputs" / "term_statistics.json"
    )

    tfidf, doc_lengths, normalized = compute_all(stats)

    print_matrix("TF-IDF", tfidf)
    print_doc_lengths(doc_lengths)
    print_matrix("NORMALIZED TF-IDF", normalized)

    save_tfidf(
        root / "outputs" / "tfidf.json",
        tfidf,
        doc_lengths,
        normalized
    )

    print("\nTF-IDF saved successfully!")


if __name__ == "__main__":
    main()