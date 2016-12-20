import pickle


def get_classifier():
    with open("serialized_classifier.txt", "rb") as f:
        classifier = pickle.load(f)

    return classifier


def get_input_type(m_string):
    return get_classifier().classify(m_string)