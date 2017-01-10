import nltk
from nltk.tag import pos_tag


def parser(text):
    if len(text) is 0:
        return None

    words = text.split()
    sentence = pos_tag(words)

    grammar = '''
    Action: {<VB|VBD|VBG|VBN|VBP|VBZ>|<VB|VBD|VBG|VBN|VBP|VBZ><VB|VBD|VBG|VBN|VBP|VBZ>|<VB|VBD|VBG|VBN|VBP|VBZ>.+<VB|VBD|VBG|VBN|VBP|VBZ>+}
    Location: {<IN><NN.*>+}
    Subject: {<JJ>*<NN|NNS|NNP|NNPS|PRP>|<PRP$><JJ*><NN|NNS|NNP|NNPS|PRP>}
    '''
    cp = nltk.RegexpParser(grammar, "Input")
    result = cp.parse(sentence)

    keys = []
    for word in result:
        if isinstance(word, nltk.tree.Tree):

            if word.label() == 'Subject':
                keys.append((word[0][0], word[0][1], 'Subject'))

            elif word.label() == 'Action':
                keys.append((word[0][0], word[0][1], 'Action'))

    return keys

    # print(parser("hello my are team"))
