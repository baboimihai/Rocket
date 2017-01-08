from KB.KnowledgeBase.AimlCommunication import Parser
#import PreProcessing.main

parser = Parser("nume")
def MainBrain(input):
    try:
        result=parser.findPattern(input);
        if result is None:
            return "Nu stiu"
        else:
            return result
    except Exception as e:
        return str(e)



    #return

    # while True:
    #     pattern = input("Me> ")
    #     #TODO: goodbye synonims
    #     result = parser.findPattern(pattern)
    #     print(result)
    # return "raspuns"
