from urlparse import urlparse
import string
import re




def swapOutDashesForUnderscores(modify):
    dashLetter = re.compile('-')
    return dashLetter.sub("_", modify)
        
def findWordGroups (modify):
    wordSets = re.compile('[a-z_]+')
    return wordSets.findall(modify)
        
def findEpisodeNumber (modify):
    numberSet = re.compile('[0-9]+')
    episodeNumber = fixEpisodeNumber (numberSet.findall(modify)[0])
    return episodeNumber

# to preserve order 9 > 09. 10 stays 10
def fixEpisodeNumber (modify):
    if len(modify) < 2:
        return "0" + modify 
    return modify

def upperAfterUnderscore (modify):
    after = False
    myList = list(modify)
    for i in xrange (0, len(myList)):
        if after == True or (i == 0 and myList[i] != "_"):
            myList[i] = str.capitalize(myList[i])
            
            after = False
        if myList[i] == "_":
            after = True
    if myList[len(myList)-1] == "_":
        myList.pop(len(myList)-1)
    return "".join(myList)

def generateMultipleLivestreamerCommandLine(parsedList):
    completeCommand = ""
    index = 0
    for item in parsedList:
        nextCommand = generateLivestreamerCommand(parsedList, index)
        completeCommand = completeCommand + nextCommand
        index = index + 1
    return completeCommand

def generateLivestreamerCommand (parsedList, index):
    show = parsedList[index][0]
    title = parsedList[index][1]
    number = parsedList[index][2]
    url = parsedList[index][3]

    return "livestreamer -o " + show + "_" + number + title + ".mp4 " + url + " best; " 


def getURLs():
    listOfURLs = []
    while True:
        print "Paste & Enter a URL or type Done"
        userInput = raw_input()
        if (userInput == "done" or userInput == "Done" or userInput == ""):
            break
        listOfURLs.append(userInput)
    return listOfURLs

def parseOneURL(fullURL):
    o = urlparse(fullURL)
    urlPath = o.path

    urlPath = swapOutDashesForUnderscores(urlPath)
    wordGroups = findWordGroups(urlPath)
    ShowName = upperAfterUnderscore(wordGroups[0])
    EpisodeTitle = upperAfterUnderscore(wordGroups[2])
    EpisodeNumber = findEpisodeNumber (urlPath)
    return [ShowName, EpisodeTitle, EpisodeNumber, fullURL]

def parseURLs (listOfURLs):
    
    i = 0
    for url in listOfURLs:
        
        listOfURLs[i] = parseOneURL(url) #extracted info
        #listOfURLs[] = url #original url
        i = i + 1


    return listOfURLs


userProvidedURLs = getURLs()
parsedList = parseURLs (userProvidedURLs)
completeLivestreamerCommand = generateMultipleLivestreamerCommandLine(parsedList)

print completeLivestreamerCommand
