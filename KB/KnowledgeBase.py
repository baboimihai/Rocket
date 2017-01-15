from KB import aiml
import xml.etree.ElementTree as ET
import os

class Interface:
    kern = aiml.Kernel()
    def __init__(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        dir = os.path.join(dir,"KB")
        tree = ET.parse(os.path.join(dir,"start.xml"))
        root = tree.getroot()
        learn = root.find("category").find("template").find("learn")
        learn.text = os.path.join(dir,"standard","std-*.aiml")
        tree.write(os.path.join(dir,"start.xml"))
        self.kern.bootstrap(learnFiles=os.path.join(dir,"start.xml"), commands="load")
    def answer(self,input):
        return self.kern.respond(input)