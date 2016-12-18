from KnowledgeBase import AimlCommunication
#dupa import se apeleaza functia de init si se preia valoarea returnata, IMPORTANT!! folositi "r" inaintea stringului, poate provoca erori altfel
tree = AimlCommunication.init(r"C:\Python Workspace\AI\alfa_RocketBot.aiml")
#trimiteti prametrul returnat mai departe la functia findPattern imrepuna cu string-ul cautat. Deocamdata in mare parte este intrebarea 
answer = AimlCommunication.findPattern("what is ai",tree)
print (answer)
#exista in ductionar "context" care contiune cateva date cateva date despre discutia curenta. Irelevant momentan
print ("Topic: "+AimlCommunication.context["topic"]+"\n")
answer = AimlCommunication.findPattern("have you",tree)
print (answer)