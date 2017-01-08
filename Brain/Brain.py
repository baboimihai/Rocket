from Rocket.KB.KnowledgeBase import AimlCommunication
#import PreProcessing.main

# dupa cum am gandit primul lucru pe care ar trebui sa il stie e username-ul ca sa poata folosi info personale sau sa salveze
# in codul comentat de mai jos poti vedea cum ar putea face si salvarea intr-un fisier cu numele userului in ultima instanta
# poate poti folosi si asta

def MainBrain(input):
    parser = AimlCommunication.Parser("mihai")
    try:
        #return PreProcessing.main.pre_process_text("George?")
        return parser.findPattern(input)
    except Exception as e:
        return str(e)

# while True:
#     pattern = input("Me> ")
#     result = parser.findPattern(pattern)
#     if result is not None:
#         print("Rocket> " + result)
#     else:
#         print("Rocket> " + "I can't help you. Do you want to give me the answer?")
#         answer = input("Me> ")
#         if parser.processAnswer(answer) == "yes":
#             print("Rocket> " + "Give me the answer.")
#             answer = input("Me> ")
#             parser.saveAnswerInUserFile(answer, pattern)
#         else:
#             print("Rocket> Ok")

# MainBrain("hello")