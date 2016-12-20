import xml.etree.ElementTree as ET
import random
import glob

context = dict()

class Parser:
    filesList = ["alfa_RocketBot", "std-brain", "std-dictionary", "std-geography", "std-inventions",
                 "std-knowledge", "std-personality", "std-pickup", "std-sextalk", "std-sports"]
    rootList = []
    currentUser = ""
    userRoot = ""
    yesNoRoot = ""
    def __init__(self, username):
        self.processAimlFiles()
        self.currentUser = username

        tree = ET.parse("aiml/yes-no.aiml")
        self.yesNoRoot = tree.getroot()

        if self.searchForFile(username) is True:
            userTree = ET.parse("aiml/user_definitions/" + username.lower() + '.aiml')
            self.userRoot = userTree.getroot()
        else:
            self.createAimlFileForUser(username.lower())

        context["it"] = ""
        context["topic"] = ""

    def processAimlFiles(self):
        # IMPORTANT!! folositi "r" inaintea stringului, poate provoca erori altfel ?
        for file in self.filesList:
            tree = ET.parse("aiml/" + file + ".aiml")
            self.rootList.append(tree.getroot())

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
        #TODO: process <srai>, <think>, <that>, <get name>
        for categ in currentRoot:
            if (categ.tag == "category"):
                for pat in categ:
                    #TODO: improve search by using reg expressions
                    if pat.tag == "pattern" and (pat.text is not None and pat.text.lower() == pattern.lower()):
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

    def processAnswer(self, text):
        return self.findPatternInCurrentRoot(text, self.yesNoRoot)

    # cauta arhiva pentru un user
    def searchForFile(self, username):
        filename = username.lower() + ".aiml"
        for file in glob.glob("aiml/user_definitions/*"):
            file = file[22:]
            if filename == file.lower():
                print("found")
                return True

    def createAimlFileForUser(self, username):
        fo = open("aiml/user_definitions/"+username+".aiml", "w")
        fo.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml version=\"1.0\">\n")
        fo.write("</aiml>")
        fo.close()

    def saveAnswerInUserFile(self, answer, question):
        fo = open("aiml/user_definitions/" + self.currentUser + ".aiml", "r+")
        fo.seek(0, 2)
        size = fo.tell()
        fo.truncate(size - 7)  # truncate </aiml>
        fo.seek(0, 2)
        fo.write("<category><pattern>" + question + "</pattern>\n<template>" + answer + "</template>\n</category>\n");
        fo.write("</aiml>")
        fo.close()

        self.userRoot = ET.parse("aiml/user_definitions/" + self.currentUser.lower() + '.aiml').getroot()


#exista in ductionar "context" care contiune cateva date cateva date despre discutia curenta. Irelevant momentan
#print ("Topic: "+AimlCommunication.context["topic"]+"\n")