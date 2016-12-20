import pickle


def get_classifier():
    with open("C:\\Users\\Baboias\\PycharmProjects\\AI_Rocket\\PreProcessing\\serialized_classifier.txt", "rb") as f:
        classifier = pickle.load(f)

    return classifier


def get_input_type(m_string):
    return get_classifier().classify(m_string)