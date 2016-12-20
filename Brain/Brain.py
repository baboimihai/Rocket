from KB.KnowledgeBase import AimlCommunication
from PreProcessing.main import pre_process_text

# print(pre_process_text("How old is George?"))
print("gata")
def MainBrain():
    print("Rocket> Who are you?")
    username = input("Me> ")
    parser = AimlCommunication.Parser(username)

    while True:
        pattern = input("Me> ")
        #TODO: goodbye synonims
        result = parser.findPattern(pattern)
        print(result)
MainBrain()
