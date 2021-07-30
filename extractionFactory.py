import json, CommentAgregator
# All logic for JSON extraction here.

def parsePrintJSON(response, level=0):
    for key in response:
        print("\t" * level + key)
        if type(response[key]) == dict:
            parsePrintJSON(response[key], level + 1)
        elif type(response[key]) == str:
            try:
                print("\t" * (level + 1) + str(response[key]))
            except UnicodeEncodeError:
                print("\t" * (level + 1) + str(response[key].encode('utf-8')))
        elif type(response[key]) == list or type(response[key]) == tuple:
            for item in response[key]:
                parsePrintJSON(item, level + 1)
        elif type(response[key]) != str:
            try:
                print("\t" * (level + 1) + str(response[key]))
            except UnicodeEncodeError:
                print("\t" * (level + 1) + str(response[key].encode('utf-8')))
# parsePrintJSON shows the formatting of the JSON from YT API in raw form.


def dumpAllComments(response="", nextPageToken="", saveOption=False, title="No_title_found!",Vid=""):
    global comCount
    comCount = 0

    if saveOption:
        file = open(title + ".txt", 'a')

    parseJSONComments(response, title, saveOption)
    while nextPageToken is not None:
        response, nextPageToken = CommentAgregator.apiRequest(nextPageToken,Vid)
        parseJSONComments(response, title, saveOption)
        print("Done, wrote", comCount, "Comments")
    if saveOption:
        file.close()

# dumpAllComments dumps all the comments to console or to a file in a standard form... for now


# # Things to allow for Api extraction:
# 1. VideoId
# 2. textDisplay
# 3. textOriginal
# 4. authorDisplayName
# 5. authorChannelUrl
# 6. authorChannelId
# 7. canRate
# 8. likeCount
# 9. publishedAt
# 10. updatedAt
def parseJSON(response):
    for key in response:
        if key == "videoId":
            videoId = response[key]
        if key == "textDisplay":
            textDisplay = response[key]
        if key == "textOriginal":
            textOriginal = response[key]
        if key == "authorDisplayName":
            authorDisplayName = response[key]
        if key == "authorChannelUrl":
            authorChannelUrl = response[key]
        if key == "authorChannelId":
            authorChannelId = response[key]
        if key == "canRate":
            canRate = response[key]
        if key == "likeCount":
            likeCount = response[key]
        if key == "publishedAt":
            publishedAt = response[key]
        if key == "updatedAt":
            updatedAt = response[key]
            print(videoId,textDisplay,textOriginal,authorDisplayName,authorChannelUrl,authorChannelId,canRate,likeCount,publishedAt,updatedAt)

        if type(response[key]) == dict:
            parseJSON(response[key])
        elif type(response[key]) == list or type(response[key]) == tuple:
            for item in response[key]:
                parseJSON(item)


def parseJSONComments(response, title, saveOption, level=0):
    for key in response:
        if key == "textDisplay":
            text = response[key]
        if key == "likeCount":
            likeCount = response[key]
            global comCount
            comCount += 1
            try:
                print(likeCount, ":", text)
            except UnicodeEncodeError:
                print(likeCount, ":", text.encode("utf-8"))
            if saveOption:
                with open(title + ".txt", 'a') as file:
                    try:
                        file.write(str(likeCount) + " : " + text + "\n")
                    except(UnicodeEncodeError):
                        file.write((str(likeCount) + " : " + str(text.encode('utf-8')) + "\n"))
                    except:
                        file.write("~FAILED ATTEMPT AT COMMENT DUMP~\n")
        if type(response[key]) == dict:
            parseJSONComments(response[key],title,saveOption, level + 1)
        elif type(response[key]) == list or type(response[key]) == tuple:
            for item in response[key]:
                parseJSONComments(item,title,saveOption, level + 1)
# parseJSONComments is a helper function for dumpAllComments


def configFileSeek(searchString):
    with open("config.json", "r") as configFile:
        configDict = json.load(configFile)
        if searchString in configDict:
            return configDict[searchString]
        else:
            raise ("The", searchString, "was not found! Please check the config file!")
# configFileSeek extracts a given item from the config file based on the searchString
