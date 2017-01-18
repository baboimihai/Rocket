from KB import KnowledgeBase

interface = KnowledgeBase.Interface()

while (True):
    inpt = input("> ")
    print(interface.answer(inpt))