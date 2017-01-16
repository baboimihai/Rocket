import os
#cauta in aiml un string
path  = os.path.dirname(__file__)
path = os.path.join(path,"standard")
for (root,directory,files) in os.walk(path):
    for file in files:
        fullFileName = os.path.join(root,file)
        print (fullFileName)
        f = open(fullFileName)
        text = f.read()
        if("What is your favorite color" in text):
            print ("found")