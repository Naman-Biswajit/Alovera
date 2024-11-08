import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from utils import duration

class YT_Data():
    def __init__(self):
        load_dotenv()
        self.youtube = build("youtube", "v3", developerKey=os.environ.get("API_KEY"))
        self.searcher = self.youtube.search()
        self.channels = self.youtube.channels()
        self.videos = self.youtube.videos()
    
    def channel_logo(self, channel_id, resolution: str = "default"):
        req = self.channels.list(id=channel_id, part="snippet")
        response = req.execute()
        return response["items"][0]["snippet"]["thumbnails"][f"{resolution}"]["url"]
    
    def format_data(self, data: str, single_request=False):
        
        processed = []
        
        for item in data["items"]:
            if single_request:
                kind = item["kind"].split('#')[1]
                id = item["id"]
            else:
                kind = item["id"]["kind"].split('#')[1]
                id = list(item["id"].keys())[1]
            
            snippet = item["snippet"]
            processed.append({
                "kind" : kind,
                "id" : id,
                "title" : snippet["title"],
                "description": snippet["description"],
                "published_at": snippet["publishedAt"],
                "channel_name": snippet["channelTitle"],
                "channel_id": snippet["channelId"],
                "upload_duration": duration(snippet["publishedAt"]),
                "thumbnail": snippet["thumbnails"]["medium"]["url"],
                "logo" : self.channel_logo(snippet["channelId"])
                })
            
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
    
    
if __name__ == "__main__":
    import json
    api = YT_Data()
    res = api.fetch_video("GwyXQO0tSW4")
    s = json.dumps(res)
    
    with open("./static/test.json", "w+") as f:
        f.write(s)