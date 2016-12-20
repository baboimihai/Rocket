# |____Prerequisites for Language detection____|

# -------------------------
# Download and install ntlk
#
# nltk - corpus,stopwords
#
# To download corpus and stopwords, if missing , run in shell:
# python
# >>import nltk
# >>nltk.download()
#
# Identifier>d
# Identifier>all-corpora

# |____Prerequisites for other____|

# -------------------------
# Download and install textblob

# pip install -U textblob
# python -m textblob.download_corpora

from autocorrect import auto_correct_input
from language_detection import detect_language
from detect_input_type import get_input_type
from synonyms import get_synonyms
from eliminate_stop_words import filter_stopwords
from parser import parser


def pre_process_text(m_input):
    if len(m_input) is 0:
        return None

    m_map = {}
    m_input = auto_correct_input(m_input)
    language = detect_language(m_input)
    m_map["language"] = language

    k = 0
    for i in filter_stopwords(m_input):
        current_dict = {}
        k += 1
        input_type = get_input_type(i)

        current_dict["type"] = input_type
        m_keys = parser(i)
        current_dict["keys"] = m_keys

        list_of_synonyms = []
        for key in m_keys:
            list_of_synonyms.append((key[0], get_synonyms(key[0])))

        current_dict["synonyms"] = list_of_synonyms

        m_map[str(k)] = current_dict

    return m_map

    # print(pre_process_text("Hello Mr. Smith, how are you doing today? How do you think python is?"))
    # return dictionary of form:
    # {'language': 'english',
    #  '1': {'synonyms': [('Hello', ['hi', 'how-do-you-do', 'hello', 'howdy', 'hullo']), ('Or', ['operating room', 'surgery', 'operating theatre', 'oregon', 'beaver state', 'or', 'operating theater'])],
    #        'type': 'q',
    #        'keys': [('Hello', 'NNP', 'Subject'), ('Or', 'NNP', 'Subject')]},
    #  '2': {'synonyms': [('Smith', ['kathryn elizabeth smith', 'david smith', 'captain john smith', 'kate smith', 'john smith', 'bessie smith', 'ian douglas smith', 'julia evelina smith', 'metalworker', 'ian smith', 'smith', 'joseph smith', 'david roland smith', 'adam smith']), ('today', ['now', 'nowadays'])],
    #        'type': 'q',
    #        'keys': [('Smith', 'NNP', 'Subject'), ('today', 'NN', 'Subject')]},
    #  '3': {'synonyms': [('think', ['recollect', 'opine', 'cogitate', 'suppose', 'reckon', 'consider', 'conceive', 'believe', 'imagine', 'mean', 'call back', 'remember', 'retrieve', 'recall', 'guess', 'call up', 'cerebrate', 'intend']), ('patron', ['frequenter', 'supporter', 'sponsor'])],
    #        'type': 'pos',
    #        'keys': [('think', 'VBP', 'Action'), ('patron', 'NN', 'Subject')]}}

    # Legend:
    # '1','2' -> sentence id
    # 'type' :q,neg,pos -> sentence type
    # 'keys' : keywords
