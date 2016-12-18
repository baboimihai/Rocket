from KnowledgeBase import AimlCommunication
tree = AimlCommunication.init(r"C:\Python Workspace\AI\alfa_RocketBot.aiml")
answer = AimlCommunication.findPattern("what is ai",tree)
print (answer)
print ("Topic: "+AimlCommunication.context["topic"]+"\n")
answer = AimlCommunication.findPattern("have you",tree)
print (answer)