import xml.etree.ElementTree as ET
import random
import string
context = dict()
def init(path):
    tree = ET.parse(path)
    context["it"] = ""
    context["topic"] = ""
    return tree


def selectRandomAnswer(rand):
    randList = list()
    for elements in rand:
        randList.append(elements.text)
    return random.choice(randList)

def processThink(thinkTag):
    context["it"]=thinkTag.find("set").find("set").text
    context["topic"] = context["it"]

def processTemplate(template):
    answer = ""
    if template.text is None:
        answer = selectRandomAnswer(template.find("random"))
    else:
        answer = template.text

    if template.find("think"):
        processThink(template.find("think"))
    return answer

def findPattern(pattern,tree):
    root = tree.getroot()
    for categ in root:
        if(categ.tag == "category"):
            for pat in categ:
                if pat.tag == "pattern" and pat.text.lower() == pattern.lower():
                    for tem in categ:
                        if(tem.tag == "template"):
                            return processTemplate(tem)
