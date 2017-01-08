from KB.KnowledgeBase import AimlCommunication
import PreProcessing.main


def MainBrain(input):
    try:
        return PreProcessing.main.pre_process_text("George?")
        #return AimlCommunication.Parser(input)
    except Exception as e:
        return str(e)



    #return

    # while True:
    #     pattern = input("Me> ")
    #     #TODO: goodbye synonims
    #     result = parser.findPattern(pattern)
    #     print(result)
    # return "raspuns"
