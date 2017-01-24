"""
Post-processing module.
Constructs a response to a question in natural language.
Recieves: the question: str (user input) - not used right now but useful for future implementations
          logic: dict, constructed by the pre-processing module. Used to construct the response using user's words.
          answer: str, as found by the brain module.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Import method: from post import obj_post_process
Usage: response = obj_post_process.construct_response(question: str, logic: dict, answer: str)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
import nltk
import random
from nltk.tokenize import word_tokenize


class PostProcess:
    def __init__(self):
        self._history = []

    def construct_response(self, question, logic, answer):
        # response = ""
        subiect = ''
        # predicat = ''
        complement = ''
        adjectiv = ("good", "cool", "great", "occasionally","bad","ugly","unregular")
        DT = ("the", "a", "this", "these", "one")
        IN = ('in', 'that')
        if 'q' in logic['type']:
            for word, part_of_speech, tip in logic['keys']:
                if part_of_speech == 'PRP' and word == 'you' or word == 'You':
                    pronoun = 'I'
                if part_of_speech == 'PRP' and word == 'I':
                    pronoun = 'You'
                if 'NN' in part_of_speech and tip == 'Subject':
                    subiect = word
                if 'VB' in part_of_speech and tip == 'Action':
                    verb = word
                if 'VBZ' in part_of_speech and tip == 'Verb':
                    complement = word
            num = random.randrange(0, 4)
            nr = random.randrange(0, 3)
            return pronoun + ' ' + verb + ' ' + subiect + ' ' + complement + ' ' + DT[nr]+' ' + adjectiv[num] + " ".join(answer) + '.'
        else:
            if 'pos' in logic["type"]:
                for word, part_of_speech, tip in logic['keys']:
                    if 'NNP' in part_of_speech and tip == 'Subject':
                        subiect = word
                    if 'VB' in part_of_speech and tip == 'Verb' and word == 'are':
                        verb = 'has'
                    if part_of_speech == 'NNS':
                        complement = word
                nr = random.randrange(len(DT) - 1)
                if len(answer) == 1:
                    return subiect + ' '+verb + ' ' + DT[-1] + ' ' + complement + ': ' + ",".join(answer) + '.'
                else:
                    return subiect + ' '+verb + ' ' + DT[nr] + ' ' + complement + ': ' + ",".join(answer) + '.'


obj_post_process = PostProcess()

if __name__ == '__main__':
    print(obj_post_process.construct_response('Tell me which are the Earth\'s oceans.',
    {'type':'pos' , 'keys': [('Earth', 'NNP', 'Subject'),('are','VB','Verb'),('oceans','NNS','subject')]},
    [' Atlantic','Pacific','Indian','Arctic','Antarctic'] ) )
    # Output: Earth has there oceans  Atlantic,Pacific,Indian,Arctic,Antarctic.


    print(obj_post_process.construct_response('What do you think python is?',
                      {'type': 'q', 'keys': [('think', 'VB', 'Action'), ('you', 'PRP', 'Subject'), ('is', 'VBZ', 'Verb'), ('python', 'NN', 'Subject')]}, [' programming language']) )
    #Output :  Python is a  cool programming language.

