class TermPositionalIndex:
    def __init__(self, token, collection_frequency, doc_positional_indexes_map, idf=1.0):
        self.token = token
        self.collection_frequency = collection_frequency
        self.doc_positional_indexes_map = doc_positional_indexes_map
        self.idf = idf


class SingleTermDocPositionalIndex:
    def __init__(self, doc_frequency, positions):
        self.doc_frequency = doc_frequency
        self.positions = positions


def positional_index_builder(
        positional_tokens, collection_positional_index, doc_id):  # generates the collection positional index according to
    # the give positional tokens
    for positional_token in positional_tokens:
        token = positional_token[0]
        if token in collection_positional_index:
            collection_positional_index[token].collection_frequency += 1
            term_positional_index = collection_positional_index[token]

            if doc_id in term_positional_index.doc_positional_indexes_map:
                term_positional_index.doc_positional_indexes_map[doc_id].doc_frequency += 1
                term_positional_index.doc_positional_indexes_map[doc_id].positions.append(positional_token[1])
            else:
                collection_positional_index[token].doc_positional_indexes_map[
                    doc_id] = SingleTermDocPositionalIndex(1, [positional_token[1]])

        else:
            collection_positional_index[token] = TermPositionalIndex(token, 1, {doc_id:
                SingleTermDocPositionalIndex(1, [positional_token[1]])})

