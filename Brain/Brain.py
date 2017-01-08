from KB.KnowledgeBase.AimlCommunication import Parser
import PreProcessing.main

parser = Parser("nume")
def MainBrain(input):
    try:
        result=parser.findPattern(input)
        vParsed=PreProcessing.main.parser(input)
        if result is None:
            return "Nu stiu"+str(vParsed)
        else:
            return result+str(vParsed)
    except Exception as e:
        return str(e)



    #return

    # while True:
    #     pattern = input("Me> ")
    #     #TODO: goodbye synonims
    #     result = parser.findPattern(pattern)
    #     print(result)
    # return "raspuns"
