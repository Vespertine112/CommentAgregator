import os
import json
import googleapiclient.discovery


def main():
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = config("APIKEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part='snippet',
        videoId=Vid,
        textFormat='plainText'
    )
    response = dict(request.execute())

    parseJSON(response)


def parseJSON(response, level=0):
    for key in response:
        print("\t" * level + key)
        if type(response[key]) == dict:
            parseJSON(response[key], level + 1)
        elif type(response[key]) == str:
            print("\t" * (level + 1) + response[key])
        elif type(response[key]) == list or type(response[key]) == tuple:
            for item in response[key]:
                parseJSON(item, level + 1)
        elif type(response[key]) != str:
            print("\t" * (level + 1) + str(response[key]))


def config(searchString):
    with open("config.json", "r") as configFile:
        configDict = json.load(configFile)
        if searchString in configDict:
            return configDict[searchString]
        else:
            raise ("The", searchString, "was not found! Please check the config file!")


if __name__ == "__main__":
    # Vid = input("Please enter the video Id you are searching for.")
    Vid = "IqQLvlKzuX8"
    main()
