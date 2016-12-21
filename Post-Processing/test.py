import nltk
from nltk.tokenize import word_tokenize
text = word_tokenize('When Mickel has passed  ? in the  these that ')
print(nltk.pos_tag(text))