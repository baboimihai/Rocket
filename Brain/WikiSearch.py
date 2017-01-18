from wikipedia import *

def highestMatch(searchCriteria, sentance):
    maxOcurance=0
    returnString=''
    sentance=sentance.split(' ')
    for word in searchCriteria:
        copy=word.split(' ')
        itOcurance=0
        for i in copy:
            for j in sentance:
                if(j==i):
                    itOcurance+=1
        if itOcurance>maxOcurance:
            returnString=word
    return returnString



def searchWiki(sentance):
    var="I don't understant what you want to say. Please rephraze."
    if not sentance:
        return var
    else:
        searchCriteria = wikipedia.search(sentance)
        toSearch=highestMatch(searchCriteria, sentance)
        returnString = wikipedia.page(toSearch)
        return returnString.url



print(searchWiki("Onion"))
