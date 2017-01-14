import xml.etree.ElementTree as ET
import random
import glob
import os

class Parser:
    filesList = ["alfa_RocketBot", "std-brain", "std-dictionary", "std-geography", "std-inventions",
                 "std-knowledge", "std-personality", "std-pickup", "std-sextalk", "std-sports"]
    rootList = []
    currentUser = ""
    userRoot = ""
    yesNoRoot = ""
    context = dict()
    directory = ""
    previousRezLen = 0
    starText = ""
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
        self.directory = os.path.dirname(os.path.dirname(__file__))
        selfDirectoryCopy = self.directory
        for path in paths:
            selfDirectoryCopy = os.path.join(selfDirectoryCopy,path)
        return selfDirectoryCopy

    #preia toate radacinile si le adauga in rootList
    def processAimlFiles(self):
        for file in self.filesList:
            path = self.getPath("aiml", file+".aiml")
            tree = ET.parse(path)
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
        #cautarile astea pot fi imbunatatite
        if(template.find("random")):
            answer = self.selectRandomAnswer(template.find("random"))
        elif (template.find("srai") is not None):
            srai = template.find("srai")
            # star ar tb verificat si in alte elemente ?
            if (srai.find("star") is not None):
                #print("srai", srai.text, srai.find("star").tail)
                text = srai.text + self.starText + srai.find("star").tail
                answer = self.findPattern(text)
            else:
                answer = self.findPattern(srai.text)
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
            print(pattern, patternTag.text)
            return True
        reverseSecond = second[::-1]
        reversePattern = pattern[::-1]
        match = reversePattern[0:len(second)]
        if(match == reverseSecond):
            self.starText = pattern[len(first)+1:-len(second)]
            # print(len(pattern[len(first)+1:-len(second)]), pattern[len(first)+1:-len(second)])
            return True
        return False

    def findPatternSimpleSearch(self, pattern, currentRoot):
        #TODO: process <star>, <think>, <that>, <get name>, <condition>
        resultTemplate = ""
        for categ in currentRoot.findall("category"):
            pat = categ.find("pattern")
            if (pat.text is not None and (pat.text == pattern.upper())):
                tem = categ.find("template")
                resultTemplate = self.processTemplate(tem)
                break

        if (resultTemplate == ""):
            return None
        return resultTemplate

    def findPatternComplexSearch(self, pattern, currentRoot):
        #TODO: process <star>, <think>, <that>, <get name>, <condition>
        resultTemplate = ""
        for categ in currentRoot.findall("category"):
            pat = categ.find("pattern")
            if (pat.text is not None and self.matchPattern(pat, pattern.upper())):
                # aici e posibil sa gasim mai multe rezultate
                if (self.previousRezLen < len(pat.text)):
                    self.previousRezLen = len(pat.text)
                    tem = categ.find("template")
                    print(tem.text)
                    resultTemplate = self.processTemplate(tem)

        if (resultTemplate == ""):
            return None
        return resultTemplate

    def findPattern(self, pattern):
        self.previousRezLen = 0
        result = self.findPatternSimpleSearch(pattern, self.userRoot)
        if result is None:
            for currentRoot in self.rootList:
                result = self.findPatternSimpleSearch(pattern, currentRoot)
                if result is not None:
                    return result
            for currentRoot in self.rootList:
                auxLen = self.previousRezLen
                auxResult = self.findPatternComplexSearch(pattern, currentRoot)
                if auxLen != self.previousRezLen:
                    result = auxResult
        return result

    def processAnswer(self, text):
        return self.findPatternSimpleSearch(text, self.yesNoRoot)

    # cauta arhiva pentru un user
    def searchForFile(self, username):
        filename = username.lower() + ".aiml"
        files = glob.glob(self.getPath("aiml","user_definitions","*"));
        for file in files:
            f = os.path.basename(file)
            if filename == f.lower():
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

    def test(self, pattern):
        print(self.findPattern(pattern))

#exista in ductionar "context" care contiune cateva date cateva date despre discutia curenta. Irelevant momentan
#print ("Topic: "+AimlCommunication.context["topic"]+"\n")