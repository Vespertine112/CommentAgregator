import os
import json
import sys, codecs
import googleapiclient.discovery
from urllib.parse import urlparse
from urllib.request import urlopen
import extractionFactory


# @author: Brayden Hill, hillbgh@gmail.com


def main(saveOption):
    response, nextPageToken = apiRequest()

    # extractionFactory.dumpAllComments(response, nextPageToken, saveOption)
    # extractionFactory.parsePrintJSON(response)
    extractionFactory.parseJSON(response)




def extractVID(link):
    link = urlparse(link)
    query = link[4]
    return query[2:]
# extracts the VID from a YT link. NEEDS FIXING FOR SOMELINKS!


def apiRequest(PageToken=""):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = extractionFactory.configFileSeek("APIKEY")

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
# sends a request to the api, returns a response


def saveOption(link):
    saveOption = str(input("Would you like to save the video?(y/n)"))
    if saveOption == 'Y' or saveOption == 'y':
        saveOption = True
    else:
        saveOption = False
    if saveOption:
        response = urlopen(link)
        rawData = response.read()
        print(rawData)

    return saveOption

# saveOption determines if the user wants to save the file, needs working on!


if __name__ == "__main__":
    link = input("Please enter the video Id you are searching for.")
    saveOption = saveOption(link)
    Vid = extractVID(link)

    # main(saveOption)
