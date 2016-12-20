from textblob.classifiers import NaiveBayesClassifier
import pickle


train_data = []
validation_data = []

# ------------------ training classifier ----------------------------
with open("affirmation_positive_training_data.txt") as pos:
    for line in pos:
        train_data.append((line, "pos"))

with open("affirmation_negative_training_data.txt") as neg:
    for line in neg:
        train_data.append((line, "neg"))

with open("question_training_data.txt") as q:
    for line in q:
        train_data.append((line, "q"))

# ------------------- validation --------------------------------------
with open("affirmation_positive_validation_data.txt") as pos:
    for line in pos:
        validation_data.append((line, "pos"))

with open("affirmation_negative_validation_data.txt") as neg:
    for line in neg:
        validation_data.append((line, "neg"))

with open("question_validation_data.txt") as q:
    for line in q:
        validation_data.append((line, "q"))


m_classifier = NaiveBayesClassifier(train_data)
serialized = pickle.dumps(m_classifier)

f = open("serialized_classifier.txt", "wb")

f.write(serialized)
f.close()

# print(m_classifier.classify("I don't like this"))
# print(m_classifier.accuracy(validation_data)) ~= 72%
