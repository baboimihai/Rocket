import nltk
from nltk.tokenize import word_tokenize
text = word_tokenize('phrase/sentence')
print(nltk.pos_tag(text))