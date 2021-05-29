# import
from gensim.models.word2vec import Word2Vec
import gensim.downloader as api
import numpy as np
import random
import string

# class


class RandomSynonymReplacement:
    def __init__(self, corpus: str, similarity_threshold: float) -> None:
        self.model = Word2Vec(api.load(corpus))
        self.similarity_threshold = similarity_threshold

    def __call__(self, text: str) -> str:
        if text[-1] in string.punctuation:
            words = text[:-1].split(' ')
        else:
            words = text.split(' ')
        for word_index in random.sample(range(len(words)), len(words)):
            word = words[word_index]
            if word.lower() in self.model.wv.key_to_index:
                similarity_word = np.array(
                    self.model.wv.most_similar(word.lower()))
                probability = similarity_word[:, 1].astype(np.float)
                similarity_index = np.where(
                    probability >= self.similarity_threshold)[0]
                if len(similarity_index):
                    words[words.index(word)] = random.sample(
                        list(similarity_word[similarity_index, 0]), 1)[0]
                    if text[-1] in string.punctuation:
                        return ' '.join(words)+text[-1]
                    else:
                        return ' '.join(words)
        return text


if __name__ == '__main__':
    # create a class of RandomSynonymReplacement
    random_synonym_replacement = RandomSynonymReplacement(
        corpus='text8', similarity_threshold=0.5)

    # define a string
    text = 'Hello, World!'

    # check the result
    print(text)
    print(random_synonym_replacement(text=text))
