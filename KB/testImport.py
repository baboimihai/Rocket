from KnowledgeBase import AimlCommunication

def talkWithTheChatbot():
    print("Rocket> Who are you?")
    username = input("Me> ")
    parser = AimlCommunication.Parser(username)
    parser.saveAnswerInUserFile(username, "What's my name?")
    print("Rocket> How do you feel today?")
    answer = input("Me> ")
    parser.saveAnswerInUserFile(answer, "How do I feel today?")
    print("Rocket> Do you want to make acquaintance?")
    answer = input("Me> ")
    if answer.lower() == "yes":
        parser.setUserProfile()
    else:
        print("Rocket> Ok then. How can I help you?")

    while True:
        print("Rocket> How can I help you?")
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
