import xml.etree.ElementTree as ET
import random
import glob
import os

context = dict()

class Parser:
    filesList = ["alfa_RocketBot.aiml", "std-brain.aiml", "std-dictionary.aiml", "std-geography.aiml", "std-inventions.aiml",
                 "std-knowledge.aiml", "std-personality.aiml", "std-pickup.aiml", "std-sextalk.aiml", "std-sports.aiml"]
    rootList = []
    currentUser = ""
    userRoot = ""
    yesNoRoot = ""

    def __init__(self, username):
        self.processAimlFiles()
        self.currentUser = username.lower()

        file_path = os.path.join(os.path.dirname(__file__), 'aiml\\' + "yes-no.aiml")
        tree = ET.parse(file_path)
        self.yesNoRoot = tree.getroot()

        if self.searchForFile(username.lower()) is True:
            file_path = os.path.join(os.path.dirname(__file__), 'aiml\\user_definitions\\' + username.lower() + '.aiml')
            userTree = ET.parse(file_path)
            self.userRoot = userTree.getroot()
        else:
            self.createAimlFileForUser(username.lower())

        context["it"] = ""
        context["topic"] = ""


    def processAimlFiles(self):
        # IMPORTANT!! folositi "r" inaintea stringului, poate provoca erori altfel ?
        for file in self.filesList:
            file_path = os.path.join(os.path.dirname(__file__), 'aiml\\' + file)
            tree = ET.parse(file_path)
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
        filename = username + ".aiml"
        file_path = os.path.join(os.path.dirname(__file__), 'aiml\\user_definitions\\*')
        for file in glob.glob(file_path):
            file = file[56:]
            if filename == file.lower():
                print("found")
                return True

    def createAimlFileForUser(self, username):
        filename = username + ".aiml"
        file_path = os.path.join(os.path.dirname(__file__), 'aiml\\user_definitions\\' + filename)
        fo = open(file_path, "w")
        fo.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml version=\"1.0\">\n")
        fo.write("</aiml>")
        fo.close()

    def saveAnswerInUserFile(self, answer, question):
        filename = self.currentUser + ".aiml"
        file_path = os.path.join(os.path.dirname(__file__), 'aiml\\user_definitions\\' + filename)
        fo = open(file_path, "r+")
        fo.seek(0, 2)
        size = fo.tell()
        fo.truncate(size - 7)  # truncate </aiml>
        fo.seek(0, 2)
        fo.write("<category><pattern>" + question + "</pattern>\n<template>" + answer + "</template>\n</category>\n");
        fo.write("</aiml>")
        fo.close()

        self.userRoot = ET.parse(file_path).getroot()


#exista in ductionar "context" care contiune cateva date cateva date despre discutia curenta. Irelevant momentan
#print ("Topic: "+AimlCommunication.context["topic"]+"\n")