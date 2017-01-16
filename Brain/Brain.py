import PreProcessing.main
from Brain.WikiSearch import searchWiki
from KB import KnowledgeBase


interface = KnowledgeBase.Interface()
def MainBrain(input):
    result = interface.answer(input)
    if result.find('I do not know')!=-1:
        result=None
    if result is not None:
        return result
    else:
        try:
            vParsed=PreProcessing.main.parser(input)
            subject=getSubject(vParsed)
            print (subject)
            response=searchWiki(subject)
            if response is not None:
                return response
            if result is None:
                return "Nu stiu"+str(vParsed)
            else:
                return result+str(vParsed)
        except Exception as e:
            return str(e)

def whatIsQuestions(input):
    whatIs="define "+input

    return interface.answer(whatIs)


def getSubject(obiect):
    subject = ''
    for i in obiect:
        for j in range(len(i)):
            if i[j] == 'Subject':
                subject = i[0]

    if(subject is not ''):
        if (not subject[len(subject) - 1].isalpha()):
            subject = subject[:-1]

    return subject

#print(PreProcessing.main.parser(input))

print(MainBrain('What is abbacus?'))

    #return

    # while True:
    #     pattern = input("Me> ")
    #     #TODO: goodbye synonims
    #     result = parser.answer(pattern)
    #     print(result)
    # return "raspuns"
