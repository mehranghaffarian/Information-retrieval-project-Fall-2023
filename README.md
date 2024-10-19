Here’s a shortened version of the **README** for your project:

---

# Persian Text Search Engine

## Project Overview
This project involves building a search engine to retrieve Persian news articles. The system processes queries and returns relevant documents using a vector space model with TF-IDF weighting. The project includes data preprocessing, index creation, and query processing.

## Features

1. **Index Creation**
   - **Dataset**: Persian news articles (JSON format).
   - **Tokenization**: Split text into tokens, handling spaces, half-spaces, and special cases.
   - **Normalization**: Standardize text by removing diacritics, punctuation, and normalizing characters.
   - **Stopword Removal**: Remove 50 most frequent words.
   - **Stemming/Lemmatization**: Reduce words to their root form.
   - **Inverted Index**: Build a positional index to store token frequency and location.

2. **Search and Ranking**
   - **Vector Space Model**: Use TF-IDF to represent documents as vectors.
   - **Similarity Measurement**: Apply cosine similarity to rank documents based on the query.

3. **Performance Optimizations (Optional)**:
   - **Champions List**: Precompute top documents for faster search.
   - **Index Elimination**: Filter out non-relevant documents to enhance speed.

## How to Run

1. **Data Setup**: Load and preprocess the dataset.
2. **Query Input**: Process user queries using the same preprocessing steps.
3. **Retrieve Results**: Return and rank the most relevant documents.

## Requirements

- Python 3.9
- Libraries: NLTK, NumPy, Scikit-learn

## Report
- Test with simple and complex queries is available in the relevant reports.

---
