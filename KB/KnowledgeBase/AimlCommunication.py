import xml.etree.ElementTree as ET
import random
import glob

context = dict()

class Parser:
    rootList = []
    currentUser = ""
    userRoot = ""
    def __init__(self, username):
        #IMPORTANT!! folositi "r" inaintea stringului, poate provoca erori altfel ?
        tree = ET.parse("aiml/alfa_RocketBot.aiml")
        self.rootList.append(tree.getroot())

        self.currentUser = username
        if self.searchForFile(username) is True:
            userTree = ET.parse("aiml/user_definitions/" + username.lower() + '.aiml')
            self.userRoot = userTree.getroot()

        context["it"] = ""
        context["topic"] = ""

    def selectRandomAnswer(self, rand):
        randList = list()
        for elements in rand:
            randList.append(elements.text)
        return random.choice(randList)

    def processThink(self, thinkTag):
        context["it"]=thinkTag.find("set").find("set").text
        context["topic"] = context["it"]

    def processTemplate(self, template):
        answer = ""
        if template.text is None:
            answer = self.selectRandomAnswer(template.find("random"))
        else:
            answer = template.text

        if template.find("think"):
            self.processThink(template.find("think"))
        return answer

    def findPatternInCurrentRoot(self, pattern, currentRoot):
        for categ in currentRoot:
            if (categ.tag == "category"):
                for pat in categ:
                    if pat.tag == "pattern" and pat.text.lower() == pattern.lower():
                        for tem in categ:
                            if (tem.tag == "template"):
                                return self.processTemplate(tem)

    def findPattern(self, pattern):
        result = self.findPatternInCurrentRoot(pattern, self.userRoot)
        if result is None:
            for currentRoot in self.rootList:
                result = self.findPatternInCurrentRoot(pattern, currentRoot)
                if result is not None:
                    return result
        else:
            return result

    #TODO: creaza noi fisiere aiml pentru fiecare nou utilizator

    # cauta arhiva pentru un user
    def searchForFile(self, username):
        filename = username.lower() + ".aiml"
        for file in glob.glob("aiml/user_definitions/*"):
            file = file[22:]
            if filename == file.lower():
                print("found")
                return True

#exista in ductionar "context" care contiune cateva date cateva date despre discutia curenta. Irelevant momentan
#print ("Topic: "+AimlCommunication.context["topic"]+"\n")