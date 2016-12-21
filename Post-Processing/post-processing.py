import nltk
import random

from nltk.tokenize import word_tokenize

def  construct_respons(quest,logic,answer):


    respons=""
    subiect=''
    predicat=''
    complement=''
    adjectiv= ("good", "cool", "great", "occasionally")
    DT=("the", "a","these")
    IN=('in','that')
    if  'g' in logic['type']:
        for word,part_of_speech,type in logic['keys'] :
            if part_of_speech=='PRP' and word=='you' or word=='You' :
                pronoun='I'
            if part_of_speech=='PRP' and word == 'I':
                pronoun = 'You'
            if 'NN' in part_of_speech and type=='Subject':
                subiect=word
            if 'VB' in part_of_speech and type=='Action':
                verb=word
            if 'VBZ' in part_of_speech and type =='Verb':
                complement=word
        num = random.randrange(0, 4)
        nr=random.randrange(0,3)
        respons= pronoun+' '  + verb + ' ' + subiect + ' '+ complement +' '+ DT[nr]+' ' + adjectiv[num]+ " ".join(answer) +'.'
    else :
        if 'pos' in logic["type"]:
            for word, part_of_speech, type in logic['keys']:
                if 'NNP' in part_of_speech and type=='Subject':
                    subiect=word
                if 'VB' in part_of_speech and type=='Verb' and word=='are'  :
                    verb='has'
                if  part_of_speech=='NNS' :
                    complement=word
            nr=random.randrange(0,3)
            respons =subiect + ' '+verb + ' ' + DT[nr] +' ' +complement+' '+ ",".join(answer) + '.'

    print(respons)


#construct_respons('Tell me which are the Earth oceans .',
#{'type':'pos' , 'keys': [('Earth', 'NNP', 'Subject'),('are','VB','Verb'),('oceans','NNS','subject')]},
#[' Atlantic','Pacific','Indian','Arctic','Antarctic'] )
# Output: Earth has there oceans  Atlantic,Pacific,Indian,Arctic,Antarctic.


#construct_respons('What do you think python is? .',
#[('python', 'NN', 'Subject'),{'type':'q' , 'keys':('think', 'VB', 'Action'),('you','PRP','Subject'),('is','VBZ','Verb')]},
#[' programming language'])
#Output :  Python is a  cool programming language.

