import logging

from flask import Flask
from flask import render_template, request, redirect, url_for

from data import YT_Data


app = Flask(__name__, template_folder="../templates", static_folder="../static")
api = YT_Data()
logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.DEBUG,  # Logging level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)


@app.route("/")
def home():
    search_response = api.search("3Blue1Brown")
    return render_template("home.html", response=search_response)

@app.route("/watch")
def player():
    id = request.args.get("play")
    is_playlist = request.args.get("playlist", "false").lower()
    index = int(request.args.get("index", "1"))
    
    if is_playlist == "true":
        is_playlist = True
        tag_query = "videoseries?list="
        response = api.fetch_playlist(id)
        
    else:
        is_playlist = False
        tag_query = ""
        response = api.fetch_video(id)
        
    response = response[0]
    logging.debug(response, tag_query)
    logging.debug(id)
    
    return render_template("player.html", search_tag=tag_query, id=id, video=response, playlist=is_playlist)

@app.route("/search")
def search():
    
    search_query = request.args.get("q")
    search_results = api.search(search_query)

    return render_template("search.html", query=search_query, response=search_results)

# for testing and rewriting index folder: 
@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=1)