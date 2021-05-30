# import
from gensim.models.word2vec import Word2Vec
import gensim.downloader as api
import numpy as np
import random
import string

# class


class RandomSynonymReplacement:
    def __init__(self, corpus: str, similarity_threshold: float) -> None:
        self.model = Word2Vec(api.load(corpus))  # create the model of Word2Vec
        self.similarity_threshold = similarity_threshold    # set the threshold

    def __call__(self, text: str) -> str:
        # Split the input text with spaces to get each word
        # and check if the last character is a punctuation mark
        if text[-1] in string.punctuation:
            words = text[:-1].split(' ')
        else:
            words = text.split(' ')

        # randomly select a word and replace it with a synonym
        for word_index in random.sample(range(len(words)), len(words)):
            word = words[word_index]
            # turn the selected word to lower case
            # and check it whether exist in the vocabulary of the Word2Vec model
            if word.lower() in self.model.wv.key_to_index:
                # get similarity word by the model of Word2Vec
                # and put it to numpy array
                similarity_word = np.array(
                    self.model.wv.most_similar(word.lower()))
                # get the similarity from similarity_word
                similarity = similarity_word[:, 1].astype(np.float)
                # get the index with similarity above the threshold
                similarity_index = np.where(
                    similarity >= self.similarity_threshold)[0]
                # check the length of similarity_index
                if len(similarity_index):
                    # randomly select the synonym
                    words[words.index(word)] = random.sample(
                        list(similarity_word[similarity_index, 0]), 1)[0]
                    # check if the last character is a punctuation mark
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
