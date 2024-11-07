import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from utils import duration

class YT_Data():
    def __init__(self):
        load_dotenv()
        self.youtube = build("youtube", "v3", developerKey=os.environ.get("API_KEY"))
        self.searcher = self.youtube.search()
        self.videos = self.youtube.videos()
    
    def format_data(self, data: str, single_request=False):
        
        processed = []
        
        for item in data["items"]:
            if single_request:
                kind = item["kind"].split('#')[1]
            else:
                kind = item["id"]["kind"].split('#')[1]
            
            snippet = item["snippet"]
            id = item["id"]
            
            processed.append({
                "kind" : kind,
                "id" : id,
                "title" : snippet["title"],
                "description": snippet["description"],
                "published_at": snippet["publishedAt"],
                "channel_name": snippet["channelTitle"],
                "channel_id": snippet["channelId"],
                "upload_duration": duration(snippet["publishedAt"]),
                "thumbnail": snippet["thumbnails"]["medium"]["url"]
                })
            
        print(str(processed[0]["description"]))
        return processed
    
        
    def search(self, query, part="snippet", **params):
        req = self.searcher.list(q=query, part=part, **params)
        results = req.execute()
        results = self.format_data(results)
        return results
    
    def fetch_video(self, query, part="snippet"):
        req = self.videos.list(id=query, part=part)
        results = req.execute()
        results = self.format_data(results, single_request=True)
        return results
    