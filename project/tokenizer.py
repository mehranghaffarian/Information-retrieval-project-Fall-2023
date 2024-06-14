from hazm import *


def stem(word: str):
    ends = [
        "ات",
        "ان",
        "ترین",
        "تر",
        "م",
        "ت",
        "ش",
        "یی",
        "ی",
        '⁩',
        "ها",
        "‌",
    ]

    if word.endswith("ۀ"):
        word = word[:-1] + "ه"

    for end in ends:
        if word.endswith(end):
            word = word[:-len(end)]
            break

    return word


class Tokenizer:
    def __init__(self):
        self.normalizer = Normalizer()
        self.lemmatizer = Lemmatizer()

    def tokenize(self, doc_content):
        doc_content = self.normalizer.normalize(doc_content)
        doc_content = word_tokenize(doc_content)

        useful_tokens = []
        for j in range(len(doc_content)):
            token = doc_content[j]

            if token in ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '?',
                         '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '《', '؛', '،', ""]:
                continue

            token = stem(token)
            useful_tokens.append((self.lemmatizer.lemmatize(token), j))

        return useful_tokens

    def first_doc_tokenize(self, doc_content):
        changed_after_lemmatization = []
        changed_after_normalization = []

        doc_content = word_tokenize(doc_content)
        all_tokens = []

        useful_tokens = []
        for j in range(len(doc_content)):
            token = doc_content[j]
            all_tokens.append(token)

            if token in ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '?',
                         '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '《', '؛', '،', ""]:
                continue

            if token != self.normalizer.normalize(token):
                changed_after_normalization.append((token, self.normalizer.normalize(token)))
                token = self.normalizer.normalize(token)

            if token != self.lemmatizer.lemmatize(stem(token)):
                changed_after_lemmatization.append((token, self.lemmatizer.lemmatize(stem(token))))

            token = stem(token)
            final_token = self.lemmatizer.lemmatize(token)
            useful_tokens.append((final_token, j))

        print("all")
        print(all_tokens)
        print("lemmatization")
        print(changed_after_lemmatization)
        print("normalization")
        print(changed_after_normalization)


        return useful_tokens
