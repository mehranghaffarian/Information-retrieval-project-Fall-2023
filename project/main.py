import json
import math
import sys
import time
import pickle

from positional_index import positional_index_builder
from tokenizer import Tokenizer


file = open("./IR_data_news_12k.json")
data = json.load(file)

tokenizer = Tokenizer()

collection_positional_index = {}
champions_map = {}
initial_tokens = []
initial_doc_removed_tokens = []
count = 0

start_time = time.time()

print("press 1 to precess the documents or press 2 to load the saved index")
if int(input()) == 2:
    with open('positional_index.pkl', 'rb') as inp:
        collection_positional_index = pickle.load(inp)
        print("loading index finished in ", time.time() - start_time)
else:
    for doc_id in data:
        print("tokenizing document: " + doc_id)
        # first_doc = data[doc_id]

        # if doc_id == '4092':
        #     initial_tokens = tokenizer.first_doc_tokenize(data[doc_id]['content'])

        tokens = tokenizer.tokenize(data[doc_id]['content'])
        positional_index_builder(tokens, collection_positional_index, doc_id)

    print("processing the documents finished in ", time.time() - start_time)
    start_time = time.time()

    term_with_frequency = [(collection_positional_index[term].collection_frequency, term) for term in
                           collection_positional_index]
    term_with_frequency.sort(reverse=True)

    print(term_with_frequency[0:50])

    for term in term_with_frequency[0:50]:
        # for doc_id in collection_positional_index[term[1]].doc_positional_indexes_map:
        #     if doc_id == '4092':
        #         initial_doc_removed_tokens.append(term[1])

        collection_positional_index.pop(term[1])

    print("the 50 most frequent tokens removed in ", time.time() - start_time)
    print(initial_doc_removed_tokens)

start_time = time.time()

# three_least_document = []
# for term in collection_positional_index:
#     three_least_document.append((len(collection_positional_index[term].doc_positional_indexes_map), term))
#
# three_least_document.sort()
# print(three_least_document[0:3])
#
# for doc_id in collection_positional_index[three_least_document[1][1]].doc_positional_indexes_map:
#     print(three_least_document[1][1])
#     print("doc_id ", doc_id)
#     print(collection_positional_index[three_least_document[1][1]].doc_positional_indexes_map[doc_id].positions)

tf_idf = {term: {} for term in collection_positional_index}
collection_size = len(data)
documents_length_square = {doc_id: 0 for doc_id in data}

for term in collection_positional_index:
    term_positional_index = collection_positional_index[term]
    doc_positional_indexes_map = term_positional_index.doc_positional_indexes_map

    term_positional_index.idf = math.log(collection_size / len(doc_positional_indexes_map))

    for term_doc_id in doc_positional_indexes_map:
        term_doc_frequency = doc_positional_indexes_map[term_doc_id].doc_frequency
        term_tf = (1 + math.log(term_doc_frequency))

        tf_idf[term][term_doc_id] = term_tf * term_positional_index.idf
        documents_length_square[term_doc_id] += term_tf ** 2


print("calculating tf-idf and documents length finished in ", time.time() - start_time)
# print("the length of tf-idf: ", len(tf_idf))
tf_idf_list = [(collection_positional_index[term].idf, term) for term in collection_positional_index]
tf_idf_list.sort()

print(f"token with most idf is {tf_idf_list[-11][1]} with the idf {tf_idf_list[-1][0]}")
print(f"token with least idf is {tf_idf_list[0][1]} with the idf {tf_idf_list[0][0]}")
# initial_tokens_idfs = []
# for token in initial_tokens:
#     token = token[0]
#     if token in collection_positional_index:
#         initial_tokens_idfs.append((collection_positional_index[token].idf, token))
#
# initial_tokens_idfs.sort()
# print(f"token with most idf is {initial_tokens_idfs[-1][1]} with the idf {initial_tokens_idfs[-1][0]}")
# print(f"token with least idf is {initial_tokens_idfs[0][1]} with the idf {initial_tokens_idfs[0][0]}")


start_time = time.time()

for term in collection_positional_index:
    doc_positional_indexes_map = collection_positional_index[term].doc_positional_indexes_map
    docs = [(doc_positional_indexes_map[doc_id].doc_frequency, doc_id) for doc_id in doc_positional_indexes_map]
    docs.sort(reverse=True)

    champions_map[term] = {}
    term_champions_list = champions_map[term]

    minimum_desired_point = docs[0][0] / 2
    median_index = 1

    while median_index < len(docs) and (docs[median_index][0] > minimum_desired_point or median_index < 200):
        median_index += 1

    for doc_frequency_id in docs[0:median_index]:
        term_champions_list[doc_frequency_id[1]] = doc_frequency_id[0]

# print("champions list created in ", time.time() - start_time)

print("Please enter the query: ")
# query = data['4092']['content']
# print(f"query is {query}")
query = input()

query_tokens = tokenizer.tokenize(query)
query_tokens_tf = {}
query_length_squared = 0

for positional_term in query_tokens:
    term = positional_term[0]

    if term in query_tokens_tf:
        query_tokens_tf[term] += 1
    else:
        query_tokens_tf[term] = 1

start_time = time.time()
docs_points = {}

for term in query_tokens_tf:
    query_term_frequency = query_tokens_tf[term]
    query_length_squared += query_term_frequency ** 2

    if term not in collection_positional_index:
        continue

    term_champions_map = champions_map[term]

    for doc_id in term_champions_map:
        if doc_id in docs_points:
            docs_points[doc_id] += tf_idf[term][doc_id] * (1 + math.log(query_term_frequency))
        else:
            docs_points[doc_id] = tf_idf[term][doc_id] * (1 + math.log(query_term_frequency))

docs_points_list = [(docs_points[doc_id] / documents_length_square[doc_id], doc_id) for doc_id in docs_points]
docs_points_list.sort(reverse=True)

# print("documents point calculated in ", time.time() - start_time)

showed_docs = 0
returned_docs = 5

# for term in query_tokens_tf:
#     if term not in collection_positional_index:
#         continue
#
#     print(f"term: {term}, idf: {collection_positional_index[term].idf}")

while returned_docs != -1:
    if showed_docs >= len(docs_points_list):
        print("run out of docs")
        break

    for i in range(showed_docs, returned_docs):
        doc_id = docs_points_list[showed_docs][1]
        print(f"{i + 1}. doc length: {len(data[doc_id]['content'])},  point: {docs_points_list[showed_docs][0]}, title: {data[doc_id]['title']}, URL: {data[doc_id]['url']}")
        # print(data[doc_id]['content'])
        showed_docs += 1

    print("Press 1 to continue, or press 0 to finish")
    if int(input()) == 0:
        returned_docs = -1
    else:
        showed_docs = returned_docs
        returned_docs += 5

save_collection = 0

print("if you want to save the collection index press 1 otherwise press 0: ")
if int(input()) == 1:
    with open('positional_index.pkl', 'wb') as output:
        pickle.dump(collection_positional_index, output, pickle.HIGHEST_PROTOCOL)
