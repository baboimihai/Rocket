import xml.etree.ElementTree as ET
import random
import glob
import os
import re

class Parser:
    filesList = []
    rootList = []
    currentUser = ""
    userRoot = ""
    yesNoRoot = ""
    context = dict()
    directory = ""
    previousRezLen = 0
    starText = ""
    def __init__(self, username):
        self.filesList = self.make_fileList()
        self.processAimlFiles()
        self.currentUser = username

        #tree = ET.parse(self.getPath("aiml","yes-no.aiml"))
        #self.yesNoRoot = tree.getroot()

        if self.searchForFile(username) is True:
            userTree = ET.parse(self.getPath("aiml","user_definitions" , username.lower() + '.aiml'))
            self.userRoot = userTree.getroot()
        else:
            self.createAimlFileForUser(username.lower())

        self.context["it"] = ""
        self.context["topic"] = ""

    def tagTextIsEmpty(self,str):
        if str is None:
            return None
        if re.match("\s+$", str):
            return True
        else:
            return False
    def  getPath(self,*paths):
        self.directory = os.path.dirname(os.path.dirname(__file__))
        selfDirectoryCopy = self.directory
        for path in paths:
            selfDirectoryCopy = os.path.join(selfDirectoryCopy,path)
        return selfDirectoryCopy

    def make_fileList(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "aiml")
        self.filesList = [f[:-5] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return self.filesList

    #preia toate radacinile si le adauga in rootList
    def processAimlFiles(self):
        for file in self.filesList:
            path = self.getPath("aiml", file+".aiml")
            try:
                tree = ET.parse(path)
                self.rootList.append(tree.getroot())
            except Exception as e:
                print("error here ",file)

    def selectRandomAnswer(self, rand):
        randList = list()
        for elements in rand:
            randList.append(elements)
        return random.choice(randList)

    def processThink(self, thinkTag):
        answer = self.processSet(thinkTag[0])


    #seteaza in dictionarul context valori si retruneaza textul din interiorul tagului + textul pana la urmatorul tag
    #schimbat sa mearga pe set in set
    def processSet(self,setTag):
        attributes = setTag.attrib
        text = ""
        if(self.tagTextIsEmpty(setTag.text) is not False):
            #daca nu are text apleaza functia de procesareSet pana cand se gaseste text
            #cand se gaseste text inseamna ca e ultimul descendend
            text = self.processSet(setTag.find("set"))
        else:
            text = setTag.text
        for key in attributes.keys():
            self.context[attributes[key]] = text
            #print(self.context)
        answer = ""
        answer += text
        if(self.tagTextIsEmpty(setTag.tail) is False): #folositor la preluare textului de dupa set pana la urmatorul tag cand set se afla in tagul template si nu in think
            answer +=setTag.tail
        return answer

    #la fel ca si set preia valoarea corespunzatoare din dictionar la care se adauga textul de dupa get
    def processGet(self,getTag):
        answer = ""
        try:
            answer = self.context[getTag.attrib["name"]]
            if(getTag.tail is not None):
                answer+=getTag.tail
        except:
            return None
        return answer


    def processSrai(self,srai):
        answer = ""
        # star ar tb verificat si in alte elemente ?
        if (srai.find("star") is not None):
            print("srai", srai.text, srai.find("star").tail)
            text = srai.text + self.starText + srai.find("star").tail
            answer = self.findPattern(text)
        else:
            answer = self.findPattern(srai.text)
        return answer

    def processCondition(self,conditionTag):
        pass

    def processThat(self,thatTag):
        pass

    def processRandom(self, tag):
        liTag = self.selectRandomAnswer(tag)#alege un tag <li> random
        answer = self.callRightFunctionForThisTag(liTag)
        return answer
        #nu prea ar mai fi nevoie sa apelaz functia asta
        #din moment ce in random avem doar taguri li ca si copii (nu neparat nepoti)

    def processLi(self, tag):
        text = ""
        for elementsOfLiTag in tag:
            returned = self.callRightFunctionForThisTag(elementsOfLiTag)
            if(returned is not None):
                text+=returned
        #process other attributes of li tag
        if(tag.text is not None):
            return tag.text
        else:
            return text
    #fiecare functie de procesare a fiecarui tag va trebui sa apeleze aceasta functie
    #in caz in care mai are alte noduri interioare de procesat
    #ce am incercat sa fac a fost propriu zis parcurgerea tagurilor dar nu si procesare
    #am schimbat ici colo cate ceva si in procesare dar mai trebuie lucrat la valorile de return
    #cand se returneaza si altele :(
    def callRightFunctionForThisTag(self,tag):
        answer = ""
        if(tag.tag == "random"):
            print("random tag")
            answer = self.processRandom(tag)
        elif(tag.tag == "srai"):
            print("srai tag")
            answer = self.processSrai(tag)
        elif(tag.tag == "set"):
            print("set tag")
            answer = self.processSet(tag)
        elif(tag.tag == "get"):
            print("get tag")
            answer = self.processGet(tag)
        elif(tag.tag == "li"):
            print("li tag")
            answer = self.processLi(tag)
        elif(tag.tag == "think"):
            print("think tag")
            self.processThink(tag)
        elif(tag.tag == "that"):
            print("that tag")
            self.processThat(tag)
        elif(tag.tag == "condition"):
            print("condition tag")
            self.processCondition(tag)
        else:
            answer = "not processed tag found "+tag.tag

        return answer


    def processTemplate(self,template):
        answer = ""
        if(template.text is not None):
            answer += template.text
        for tag in template:
            returned = self.callRightFunctionForThisTag(tag)
            if returned is not None:
                answer+=returned
        return answer

    def processTemplateOld(self, template):
        answer = ""
        #cautarile astea pot fi imbunatatite
        if(template.find("random")):
            answer = self.selectRandomAnswer(template.find("random"))
            return answer
        elif (template.find("srai") is not None):
            srai = template.find("srai")
            answer = self.processSrai(srai)

        elif (template.find("set") is not None):
            if template.text is not None:
                answer = template.text
            for setTag in template.findall("set"):
                result = self.processSet(setTag)
                if(result is not None):
                    answer+= result
        else:
            answer = template.text
        #doar pentru testare
        #if(template.find("get") is not None):
            #print(self.processGet(template.find("get")))

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
            #print(pattern, patternTag.text)
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
                    #print(tem.text)
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

    def testSrai(self, pattern):
        print(self.findPattern(pattern))
    def testSet(self,pattern):
        print(self.findPattern(pattern))
    def testGet(self,pattern):
        print(self.findPattern(pattern))



#exista in ductionar "context" care contiune cateva date cateva date despre discutia curenta. Irelevant momentan
#print ("Topic: "+AimlCommunication.context["topic"]+"\n")
