import pickle
from PreProcessing.train_classifier import word_feats
import os
dir = os.path.dirname(__file__)
def get_classifier():
    with open(os.path.join(dir,"serialized_classifier.txt"), "rb") as f:
        classifier = pickle.load(f)

    return classifier


def get_input_type(m_string):
    return get_classifier().classify(word_feats(m_string))

