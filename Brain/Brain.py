import PreProcessing.main
from KB.KnowledgeBase import Parser

parser = Parser("nume")
def MainBrain(input):
    user_authenthicated=0

    result = parser.findPattern(input[:-1])
    if result is not None:
        return result
    else:
        try:
            vParsed=PreProcessing.main.parser(input)
            subject=getSubject(vParsed)
            response=whatIsQuestions(subject)
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

    return parser.findPattern(whatIs)

def getQuestionType(input): #what who when where why how
    text=input.lower()
    if text.find('what') != -1:
        return 1
    if text.find('who') != -1:
        return 2
    if text.find('when') != -1:
        return 3
    if text.find('where') != -1:
        return 4
    if text.find('why') != -1:
        return 5
    if text.find('how') != -1:
        return 6

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
    #     result = parser.findPattern(pattern)
    #     print(result)
    # return "raspuns"
