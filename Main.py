from urlparse import urlparse
import string
import re


def swapOutDashesForUnderscores(modify):
    ''' Improve legibility by substituting all - for _
    Given: food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    '''
    dashLetter = re.compile('-')
    return dashLetter.sub("_", modify)
        
def findWordGroups (modify):
    wordSets = re.compile('[a-z_]+')
    return wordSets.findall(modify)
        
def findEpisodeNumber (modify):
    ''' Given a URL extract the episode number and return it in 2-digit form
    Given: food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    Return: 09
    '''
    numberSet = re.compile('[0-9]+')
    episodeNumber = fixEpisodeNumber (numberSet.findall(modify)[0])
    return episodeNumber

def fixEpisodeNumber (modify):
    ''' Change single digit episodeNumbers to 2-digit eipsode numbers
    Given:   9
    Return: 09
    '''
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

def generateDebugURLs ():
    ''' Return a list of 3 sample URLS
    '''
    return ['http://www.crunchyroll.com/engaged-to-the-unidentified/episode-1-its-important-to-start-off-on-the-right-foot-648831',
    'http://www.crunchyroll.com/baby-steps/episode-14-moonlight-and-the-sound-of-waves-678323',
    'http://www.crunchyroll.com/food-wars-shokugeki-no-soma/episode-11-the-magician-from-the-east-678181']

def getURLsFromUser():
    ''' Accept and store raw URLS provided by the user then return all as a list
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
        if (userInput == "debug" or userInput == "Debug"): # DEBUG option for convenient testing
            listOfURLs.extend(generateDebugURLs())
            break
        elif (userInput == "done" or userInput == "Done" or userInput == ""):  # Finished input
            break
        elif ("www.crunchyroll.com" not in userInput): # Initial validation that it is a Crunchyroll URL
            raise TypeError ("Input must be a crunchyroll url")
            break
        elif ("--season" in userInput):  # Season support
            '''Determine what season they want the next set of urls or stop season mode etc.
            '''
            raise NotImplementedError
        else:                                               # Add URL to the List
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

    URLParsedObject = urlparse(fullURL)
    URLPath = URLParsedObject.path
    '''urlparse returns an object seperated into its parts. For this we only care about the .path part
    Given: http://www.crunchyroll.com/food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    The .path will be 'food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171'
    '''
    # start food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    URLPath = swapOutDashesForUnderscores(URLPath) #food_wars_shokugeki_no_soma/episode_6_the_meat_invader_678171
    wordGroups = findWordGroups(URLPath)    # [food_wars_shokugeki_no_soma, eipsode, the_meat_invader]
    ShowName = upperAfterUnderscore(wordGroups[0])
    EpisodeTitle = upperAfterUnderscore(wordGroups[2])
    EpisodeNumber = findEpisodeNumber (URLPath)
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
