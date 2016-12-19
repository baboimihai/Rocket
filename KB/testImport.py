from KnowledgeBase import AimlCommunication

# TODO: inca mai trebuie sa fac salvarea unor date in fisiere

def talkWithTheChatbot():
    print("Rocket> Who are you?")
    username = input("Me> ")
    parser = AimlCommunication.Parser(username)

    while True:
        pattern = input("Me> ")
        result = parser.findPattern(pattern)
        if result is not None:
            print("Rocket> " + result)
        else:
            print("Rocket> " + "I can't help you. Do you want to give me the answer?")
            #TODO: tratare cazuri

talkWithTheChatbot()