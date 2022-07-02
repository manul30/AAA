from ctypes.wintypes import tagSIZE
import requests
import os
import json
import pickle
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN_TWITTER = os.getenv('BEARER_TOKEN_TWITTER')

def find_query(mainWord, tags):
    if tags==[]:
        query_params = {'query': mainWord ,'tweet.fields': 'author_id'}
        return query_params    
    queryTags = ' OR '.join(map(str,tags))
    #query_params = {'query': '(from:UTECuniversidad -is:reply) OR (UTEC OR #ingenioexponencial OR presencialidad) Peru','tweet.fields': 'author_id'}
    query_params = {'query': mainWord + ' ('+ queryTags +')','tweet.fields': 'author_id'}
    return query_params

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    bearer_token = BEARER_TOKEN_TWITTER

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params, mainWord, tags):
    params = find_query(mainWord, tags)
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def twitterFind(mainWord, tags=[]):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    json_response = connect_to_endpoint(search_url, find_query,mainWord, tags)
    return json_response

#   Para leer la data del archivo data.json
#   --
#   import json
#   data = json.load(open('data.json'))
#   --
#   Para ver la data (el tweet) (iterar)
#   data['data'][i]['text']


if __name__ == "__main__":
    twitterFind('UTEC', ['opinion', 'review'])