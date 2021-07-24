import os
import json
import sys, codecs
import googleapiclient.discovery
from urllib.parse import urlparse


def main(saveOption):
    response, nextPageToken = apiRequest()
    dumpAllComments(response, nextPageToken, saveOption)

    # parsePrintJSON(response)


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


def dumpAllComments(response="", nextPageToken="", saveOption=False):
    global comCount
    comCount = 0

    if saveOption:
        file = open("comments.txt", 'a')
        file.close()
    parseJSONComments(response, saveOption=saveOption)
    while nextPageToken is not None:
        response, nextPageToken = apiRequest(nextPageToken)
        parseJSONComments(response, saveOption=saveOption)
    print("Done, wrote", comCount, "Comments")


def parseJSONComments(response, level=0, saveOption=False):
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
                with open('comments.txt', 'a') as file:
                    try:
                        file.write(str(likeCount) + " : " + text + "\n")
                    except(UnicodeEncodeError):
                        file.write((str(likeCount) + " : " + text.encode('utf-8') + "\n"))
                    except:
                        file.write("~FAILED ATTEMPT AT COMMENT DUMP~\n")
        if type(response[key]) == dict:
            parseJSONComments(response[key], level + 1, saveOption)
        elif type(response[key]) == list or type(response[key]) == tuple:
            for item in response[key]:
                parseJSONComments(item, level + 1, saveOption)


def configFileSeek(searchString):
    with open("config.json", "r") as configFile:
        configDict = json.load(configFile)
        if searchString in configDict:
            return configDict[searchString]
        else:
            raise ("The", searchString, "was not found! Please check the config file!")


def extractVID(link):
    link = urlparse(link)
    query = link[4]
    return query[2:]


def apiRequest(PageToken=""):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = configFileSeek("APIKEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part='snippet',
        videoId=Vid,
        textFormat='plainText',
        maxResults=100,
        pageToken=PageToken

    )
    response = dict(request.execute())

    try:
        return response, response["nextPageToken"]
    except:
        return response, None


def saveOption():
    saveOption = str(input("Would you like to save the video?(y/n)"))
    if saveOption == 'Y' or saveOption == 'y':
        saveOption = True
    else:
        saveOption = False
    return saveOption


if __name__ == "__main__":
    link = input("Please enter the video Id you are searching for.")
    saveOption = saveOption()
    Vid = extractVID(link)

    main(saveOption)
