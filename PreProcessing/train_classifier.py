import pickle
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def word_feats(words):
    return dict([(word, True) for word in words])
import os
dir = os.path.dirname(__file__)
negatives = open(os.path.join(dir,"negative_data.txt"),"r")
positives = open(os.path.join(dir,"positive_data.txt"),"r")
questions = open(os.path.join(dir,"question_data.txt"),"r")

negative_features = [(word_feats(negative.split()),'neg') for negative in negatives.readlines()]
positive_features = [(word_feats(positive.split()),'pos') for positive in positives.readlines()]
question_features = [(word_feats(question.split()),'q') for question in questions.readlines()]

negcutoff = len(negative_features) * 3/4
poscutoff = len(positive_features) * 3/4
question_cut_off = len(question_features) * 3/4

trainfeats = negative_features[:int(negcutoff)] + positive_features[:int(poscutoff)] + question_features[:int(question_cut_off)]
testfeats = negative_features[int(negcutoff):] + positive_features[int(poscutoff):] + question_features [int(question_cut_off):]

# print ('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

classifier = NaiveBayesClassifier.train(trainfeats)


serialized = pickle.dumps(classifier)

f = open("serialized_classifier.txt", "wb")

f.write(serialized)
f.close()

# print(classifier.classify(word_feats("Who are you ?")))
# print ('accuracy:', nltk.classify.util.accuracy(classifier, testfeats)) -> 89% accuracy