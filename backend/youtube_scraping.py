from cgitb import html
from googleapiclient.discovery import build
import json
import requests
import urllib.request
import re
import sys
import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

api_key = YOUTUBE_API_KEY

youtube = build('youtube', 'v3', developerKey=api_key)


def scrape_comments_with_replies(id):
    data = {'items':[]}                 # filtro de video con comentarios desactivados
    try:
        data = youtube.commentThreads().list(part='snippet', videoId=id, maxResults='5', textFormat="plainText").execute()
    except:
        pass
    return data

def videoSearch(search, tags, maxResults):
    if tags == []:
        query = search
    else:
        query = search.strip("\"").replace(" ","+")
        for i in tags:
            query=query+'+'+i
    video_ids=[]
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query='+query)
    #print('https://www.youtube.com/results?search_query='+query)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return video_ids[0:maxResults]


def findYoutube(mainWord, tags=[]):
    video_ids = videoSearch(mainWord, tags, 2)
    response= {}
    for i in video_ids:
        response[i] = scrape_comments_with_replies(i)
    return response

#response = findYoutube('UTEC',['opinion'])
#print(response)
#print(type(response))
#print(json.dumps(response, indent = 4))

#for i in video_ids:
    
#    scrape_comments_with_replies('youtube_comments_'+str(i)+'.json',i)

# data['items'][0]["snippet"]['topLevelComment']["snippet"]["textDisplay"]
