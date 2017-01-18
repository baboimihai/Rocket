import PreProcessing.main
from KB import KnowledgeBase
from PostProcessing.wiki_search import get_response

interface = KnowledgeBase.Interface()
def MainBrain(input):
    global isinactive
    result = interface.answer(input)
    if result[1] == ('no match'):
        genericAnswer = result[0]
    else:
        return result[0]

    try:

        vParsed=PreProcessing.main.parser(input)
        subject=getSubject(vParsed)

        if subject is not None:

            response=get_response(subject)

        if response[1] is True:

            return response[0]

        else:

            return genericAnswer

        if result is None:
            return "Nu stiu"+str(vParsed)
        else:
            return result+str(vParsed)
    except Exception as e:
        return "An error ocurred, I'm sorry maybe you want to talk about something else?"


def random_bot_line():
    result=interface.answer("RANDOM FACTS FOR WHEN THE USER IS INACTIVE")
    return (result[0]+"?")

def getSubject(obiect):
    subject = []
    for i in obiect:
        for j in range(len(i)):
            if i[j] == 'Subject':
                subject.append(i[0])


    return subject


#print(MainBrain('Do you know who trump is?'))


