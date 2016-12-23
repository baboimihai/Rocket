import pickle
from train_classifier import word_feats

def get_classifier():
    with open("serialized_classifier.txt", "rb") as f:
        classifier = pickle.load(f)

    return classifier


def get_input_type(m_string):
    return get_classifier().classify(word_feats(m_string))

