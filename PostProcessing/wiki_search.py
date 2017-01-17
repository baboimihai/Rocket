
import wikipedia
from nltk.tokenize import sent_tokenize
from Brain.WikiSearch import highestMatch

def first_sentence(sentence):
    
    searchCriteria = wikipedia.search(sentence)
    word = highestMatch(searchCriteria, sentence)

    information = str(wikipedia.summary(word).encode('utf-8'))
    sent_tokenize_list = sent_tokenize(information)
    return sent_tokenize_list[0]

print(first_sentence("onion"))

