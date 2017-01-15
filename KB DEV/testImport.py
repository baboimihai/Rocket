from KB.KnowledgeBase import AimlCommunication


def talkWithTheChatbot():
    print("Rocket> Who are you?")
    username = input("Me> ")
    parser = AimlCommunication.Parser(username)

    while True:
        pattern = input("Me> ")
        #TODO: goodbye synonims
        result = parser.findPattern(pattern)
        if result is not None:
            print("Rocket> " + result)
        else:
            print("Rocket> " + "I can't help you. Do you want to give me the answer?")
            answer = input("Me> ")
            if parser.processAnswer(answer) == "yes":
                print("Rocket> " + "Give me the answer.")
                answer = input("Me> ")
                parser.saveAnswerInUserFile(answer, pattern)
            else:
                print("Rocket> Ok")

#talkWithTheChatbot()
parser = AimlCommunication.Parser("mihai")
#teste din aiml vechi
#parser.testSrai("WHEN WAS THE FIRST TELEVISION BUILT")
#parser.testSet("WHAT DO YOU WANT TO TALK ABOUT"); # eroare
#parser.testSet("WHEN IS CHRISTMAS")
#parser.testGet("WHAT IS WRONG WITH YOU")
print("MY NAME IS SAM")
print(parser.findPattern("MY NAME IS SAM"))
print("MY NAME IS WHAT")
print(parser.findPattern("MY NAME IS WHAT"))
