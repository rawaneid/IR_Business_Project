# ===== Boolean Queries =====

def _doc_sort_key(doc_id):
    number = doc_id[1:]

    if doc_id.startswith("d") and number.isdigit():
        return (0, int(number))

    return (1, doc_id.lower())

def get_docs(index, term):
    return set(index.get(term.lower(), {}).keys())


def all_docs(index):
    docs = set()
    for postings in index.values():
        docs.update(postings.keys())
    return docs


def bool_and(index, t1, t2):
    return get_docs(index, t1) & get_docs(index, t2)


def bool_or(index, t1, t2):
    return get_docs(index, t1) | get_docs(index, t2)


def bool_not(index, term):
    return all_docs(index) - get_docs(index, term)



def boolean_search(index, query):

    tokens = query.replace("(", " ( ").replace(")", " ) ").split()

    # Combine consecutive words into phrase tokens
    processed_tokens = []
    phrase = []

    for token in tokens:

        if token.upper() in ("AND", "OR", "NOT", "(", ")"):

            if phrase:
                processed_tokens.append(" ".join(phrase))
                phrase = []

            processed_tokens.append(token)

        else:
            phrase.append(token)

    if phrase:
        processed_tokens.append(" ".join(phrase))

    tokens = processed_tokens
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def take():
        nonlocal pos
        token = tokens[pos]
        pos += 1
        return token

    def parse_or():
        result = parse_and()
        while peek() is not None and peek().upper() == "OR":
            take()
            result = result | parse_and()
        return result

    def parse_and():
        result = parse_not()
        while peek() is not None and peek().upper() == "AND":
            take()
            result = result & parse_not()
        return result

    def parse_not():
        if peek() is not None and peek().upper() == "NOT":
            take()
            return all_docs(index) - parse_not()
        return parse_atom()

    def parse_atom():
        token = peek()

        if token is None:
            raise ValueError("Query ended unexpectedly")

        if token == "(":
            take()
            result = parse_or()

            if peek() != ")":
                raise ValueError("Missing closing parenthesis")

            take()
            return result

        token = take()

        if " " in token:
            return {
                item["document"]
                for item in phrase_query(index, token)
            }

        return get_docs(index, token)

    result = parse_or()

    if pos != len(tokens):
        raise ValueError(f"Unexpected token: {tokens[pos]}")

    return sorted(result, key=_doc_sort_key)



# ===== Phrase Queries =====

def phrase_query(index, query):

    terms = query.lower().split()

    if not terms:
        return []

    # Get documents containing all query terms
    common_docs = set(index.get(terms[0], {}).keys())

    for term in terms[1:]:
        common_docs &= set(index.get(term, {}).keys())

    result = []

    # Check positions of consecutive terms
    for doc_id in common_docs:

        first_positions = index[terms[0]][doc_id]

        for position in first_positions:

            match = True

            for i in range(1, len(terms)):

                expected_position = position + i

                if expected_position not in index[terms[i]][doc_id]:
                    match = False
                    break

            if match:
                result.append({
                    "document": doc_id,
                    "starting_position": position,
                    "phrase_token_range": (
                        f"{position}-{position + len(terms) - 1}"
                    )
                })

    return sorted(
        result,
        key=lambda item: (
            _doc_sort_key(item["document"]),
            item["starting_position"]
        )
    )
