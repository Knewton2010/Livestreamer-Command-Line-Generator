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

    return "livestreamer -o " + show + "_" + number + title + " " + url + " best; " 


def getURLsFromUser():
    ''' 
    '''
    prompt = """Please provide Crunchyroll URLS. 
    You may paste each url one at a time hitting enter after each,
    or you may paste sevearl URLs at once, each sperated by an Enter
    When you have entered all the URLs you wish to process,
    press enter on a blank line or type 'Done' """
    print prompt

    listOfURLs = [] # Array of URLs to be filled with user provided URLS 
    while True:
        userInput = raw_input()
        if (userInput == "done" or userInput == "Done" or userInput == ""):
            break
        elif ("-season" in userInput or "-s" in userInput or "--season" in userInput):
            '''Determine what season they want the next set of urls or stop season mode etc.
            '''
            raise NotImplementedError
        else:
            listOfURLs.append(userInput)
    return listOfURLs

def parseOneURL(fullURL):
    ''' Given a single Crunchyroll.com url, it will format and extract the relevant information
    needed to properly name the file.
    The desired format is:
        Anime_Name_[Season Identifier]_EpisodeNum_Episode_Name
        where Season Identifier is user defined and EpisodeNum has a preceeding 0 if single digit

    Example:
    Given:  http://www.crunchyroll.com/food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    Return: Food_Wars_Shokugeki_No_Soma_06_The_Meat_Invader
    '''

    o = urlparse(fullURL)
    urlPath = o.path
    '''urlparse returns an object seperated into its parts. For this we only care about the .path part
    Given: http://www.crunchyroll.com/food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    The .path will be 'food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171'
    '''

    urlPath = swapOutDashesForUnderscores(urlPath)
    wordGroups = findWordGroups(urlPath)
    ShowName = upperAfterUnderscore(wordGroups[0])
    EpisodeTitle = upperAfterUnderscore(wordGroups[2])
    EpisodeNumber = findEpisodeNumber (urlPath)
    return [ShowName, EpisodeTitle, EpisodeNumber, fullURL]

def parseURLs (listOfURLs):  
    ''' Takes the URLS out one at a time and hands them to the 
    parseOneURL function. The newly parsed url overwrites the 
    non-parsed url. (i.e. In-place).
    '''
    i = 0
    for url in listOfURLs:
        listOfURLs[i] = parseOneURL(url) #extracted info
        i = i + 1
    return listOfURLs


''' This program has 3 distinct stages. 
1. Request a set of urls from the user and store them
2. Parse and formulate the compiled Livestreamer command
3. Return the string to the user
'''
userProvidedURLs = getURLsFromUser()
parsedList = parseURLs (userProvidedURLs)
completeLivestreamerCommand = generateMultipleLivestreamerCommandLine(parsedList)

print completeLivestreamerCommand
