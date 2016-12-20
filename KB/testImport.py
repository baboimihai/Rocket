from KnowledgeBase import AimlCommunication

# TODO: inca mai trebuie sa fac salvarea unor date in fisiere

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

talkWithTheChatbot()