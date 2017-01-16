from KB import aiml
import xml.etree.ElementTree as ET
import os

class Interface:
    kern = aiml.Kernel()
    dir = os.path.dirname(os.path.dirname(__file__))
    dir = os.path.join(dir, "KB")
    def __init__(self):
        tree = ET.parse(os.path.join(self.dir,"start.xml"))
        root = tree.getroot()
        learn = root.find("category").find("template").find("learn")
        learn.text = os.path.join(self.dir,"standard","std-*.aiml")
        tree.write(os.path.join(self.dir,"start.xml"))
        self.kern.bootstrap(learnFiles=os.path.join(self.dir,"start.xml"), commands="load")
    def answer(self,input):
        answer =  self.kern.respond(input)
        pathToNoAnswer = os.path.join(self.dir,"noAnswer")
        toReturn = list()
        toReturn.append(answer)
        with open(pathToNoAnswer) as f:
            lines = [line.rstrip('\n') for line in f]
        for line in lines:
            if line in answer:
                toReturn.append("no match")
                return toReturn
        toReturn.append("match")
        return toReturn