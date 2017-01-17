
import wikipedia
from nltk.tokenize import sent_tokenize


def first_sentence(words):
    try:
        information = wikipedia.summary(" ".join(words)).encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        sent_tokenize_list = sent_tokenize(information)
        return sent_tokenize_list[0]
    except:
        return None


def get_response(subjects):
    for i in range(len(subjects), 1, -1):
        a = first_sentence(subjects[:i])
        if a is not None:
            return [a, True]
    return ["", False]


#print(first_sentence(["President", "United States of America"]))




