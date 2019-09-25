import requests
from textblob import TextBlob
import config
from urllib.parse import urlparse, parse_qs

API_KEY = config.api_key


def getvideoID() -> int:
    '''parse videoLink to grab videoID
    '''
    videoLink = input("Enter a Youtube Link: ")
    parsedlink = urlparse(videoLink)
    return parse_qs(parsedlink.query)['v']


def loadcomments(commentload: dict, comments: list) -> None:
    '''Add all comments to a list
    '''
    for i in commentload["items"]:
        comments.append(i["snippet"]["topLevelComment"]["snippet"]["textOriginal"])


def getComments(videoID: int) -> list :
    '''uses a get request to get all comments into a list.
    '''
    commentlist = []
    result = requests.get("https://www.googleapis.com/youtube/v3/commentThreads",
                          params={
                              "key": API_KEY,
                              "part": "snippet",
                              "videoId": videoID,
                              "maxResults" : 100,
                          })
    loadcomments(result.json(),commentlist)
    while "nextPageToken" in result.json():
        pagetoken = result.json()["nextPageToken"]
        result = requests.get("https://www.googleapis.com/youtube/v3/commentThreads",
                              params={
                                  "key": API_KEY,
                                  "part": "snippet",
                                  "videoId": videoID,
                                  "maxResults": 100,
                                  "pageToken": pagetoken
                              })
        loadcomments(result.json(),commentlist)
    return commentlist


def sentimentCalc(comments: list) -> float:
    '''Calculate the average polarity score for a video
    '''
    length = len(comments)
    polarity = 0
    for i in comments:
        polarity += TextBlob(i).sentiment.polarity
    return polarity / length


video_id = getvideoID()
load = getComments(video_id)
score = sentimentCalc(load)
print(score)





