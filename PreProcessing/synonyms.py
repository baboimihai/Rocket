from nltk.corpus import wordnet
from itertools import chain


def get_synonyms(given_word):

    synonyms = wordnet.synsets(given_word)
    lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    if len(lemmas) != 0:

        final = list(lemmas)

        if given_word in final:
            final.remove(given_word)

        final = [i.lower().replace("_", " ") for i in final]
        return final

    else:
        return None
