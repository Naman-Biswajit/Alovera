import os

from dotenv import load_dotenv
from apiclient.discovery import build


load_dotenv()

class YT_Data():
    def __init__(self):
        self.youtube = build("youtube", "v3", developerKey=os.environ.get("API_KEY"))
        self.search = self.youtube.search()
    
    def reorganise(self, raw_results):
        res = {}
        res["data"] = []
        
        for item in raw_results["items"]:
            
            type = item["id"]["kind"].split("#")[1]
            id = list(item["id"].values())[1]
            
            res["data"].append({
                        "id" : id,
                        "kind" : type,
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                        "channelId": item["snippet"]["channelId"],
                        "channel": item["snippet"]["channelTitle"],
                        "publishedAt": item["snippet"]["publishedAt"]
                        })
            
        return res

    def find(self, query, part="snippet", **params):
        req = self.search.list(q=query, part=part, **params)
        results = req.execute()
        results = self.reorganise(results)
        
        return results