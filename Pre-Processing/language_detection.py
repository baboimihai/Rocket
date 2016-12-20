from nltk import wordpunct_tokenize
from nltk.corpus import stopwords


def calculate_probability(m_input):

    """
    Calculate probability of given text to be written in some languages and
    return a dictionary like : {'french': 2, 'spanish': 4, 'english': 0}

    @parameter: Text Input

    @return: Dictionary with ratios
    """

    probability = {}

    # tokenize and get words, all as lower

    tokens = wordpunct_tokenize(m_input)
    words = [word.lower() for word in tokens]

    # Counter per language included in nltk number of unique stopwords in text

    for language in stopwords.fileids():  # returns list like ["dutch", "french", etc.]

        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        probability[language] = len(common_elements)  # language "score"

    return probability


def detect_language(m_input):

        if len(m_input) is not 0:
            probabilities = calculate_probability(m_input)
            most_scored_language = max(probabilities, key=probabilities.get)

            return most_scored_language
        else:
            return None
