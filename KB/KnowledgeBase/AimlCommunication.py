import xml.etree.ElementTree as ET
import random
import glob
import os

class Parser:
    filesList = ["did-you-know","alfa_RocketBot", "std-brain", "std-dictionary", "std-geography", "std-inventions",
                 "std-knowledge", "std-personality", "std-pickup", "std-sextalk", "std-sports"]
    rootList = []
    currentUser = ""
    userRoot = ""
    yesNoRoot = ""
    context = dict()
    directory = os.path.dirname(os.path.dirname(__file__))
    def __init__(self, username):
        self.processAimlFiles()
        self.currentUser = username

        tree = ET.parse(self.getPath("aiml","yes-no.aiml"))
        self.yesNoRoot = tree.getroot()

        if self.searchForFile(username) is True:
            userTree = ET.parse(self.getPath("aiml","user_definitions" , username.lower() + '.aiml'))
            self.userRoot = userTree.getroot()
        else:
            self.createAimlFileForUser(username.lower())

        self.context["it"] = ""
        self.context["topic"] = ""

    def  getPath(self,*paths):
        selfDirectoryCopy = self.directory
        for path in paths:
            selfDirectoryCopy = os.path.join(selfDirectoryCopy,path)
        return selfDirectoryCopy

    #preia toate radacinile si le adauga in rootList
    def processAimlFiles(self):
        for file in self.filesList:
            tree = ET.parse(self.getPath("aiml", file+".aiml"))
            self.rootList.append(tree.getroot())

    def selectRandomAnswer(self, rand):
        randList = list()
        for elements in rand:
            randList.append(elements.text)
        return random.choice(randList)

    def processThink(self, thinkTag):
        self.context["it"]=thinkTag.find("set").find("set").text
        self.context["topic"] = self.context["it"]
    def processSrai(self,sraiTag):
        pass
    def processCondition(self,conditionTag):
        pass
    def processThat(self,thatTag):
        pass

    def processTemplate(self, template):
        answer = ""
        #TODO sa se verifica urmatorul tag
        if(template.find("random")):
            answer = self.selectRandomAnswer(template.find("random"))
        else:
            answer = template.text

        if template.find("think"):
            self.processThink(template.find("think"))
        return answer

    def matchPattern(self,patternTag,pattern): #face match si pe pattern care contine un singur * ex: <pattern>A BOOK *</pattern>
        star = ""
        if(patternTag is None):
            return False
        if("*" not in patternTag.text):
            return False
        poz = patternTag.text.find("*")
        first = patternTag.text[0:poz-1]
        if(first != pattern[0:poz-1]):
            return False
        second = patternTag.text[poz+1:]
        if(len(second)==0):
            return True
        reverseSecond = second[::-1]
        reversePattern = pattern[::-1]
        match = reversePattern[0:len(second)]
        if(match == reverseSecond):
            return True
        return False

    def findPatternInCurrentRoot(self, pattern, currentRoot):
        #TODO: process <srai>, <think>, <that>, <get name>, <condition>
        for categ in currentRoot.findall("category"):
            pat = categ.find("pattern")
            # TODO: improve search by using reg expressions
            if (pat.text is not None and (pat.text.lower() == pattern.lower() or self.matchPattern(pat,pattern.upper()))):
                tem = categ.find("template")
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
        files = glob.glob(self.getPath("aiml","user_definitions","*"));
        for file in files:
            f = os.path.basename(file)
            if filename == f.lower():
                print("found")
                return True

    def createAimlFileForUser(self, username):
        fo = open(self.getPath("aiml","user_definitions",username+".aiml"), "w")
        fo.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml version=\"1.0\">\n")
        fo.write("</aiml>")
        fo.close()

    def saveAnswerInUserFile(self, answer, question):
        fo = open(self.getPath("aiml","user_definitions" , self.currentUser + ".aiml"), "r+")
        fo.seek(0, 2)
        size = fo.tell()
        fo.truncate(size - 7)  # truncate </aiml>
        fo.seek(0, 2)
        fo.write("<category><pattern>" + question + "</pattern>\n<template>" + answer + "</template>\n</category>\n");
        fo.write("</aiml>")
        fo.close()

        self.userRoot = ET.parse(self.getPath("aiml","user_definitions" , self.currentUser.lower() + '.aiml')).getroot()


#exista in ductionar "context" care contiune cateva date cateva date despre discutia curenta. Irelevant momentan
#print ("Topic: "+AimlCommunication.context["topic"]+"\n")