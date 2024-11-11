from flask import Flask
from flask import render_template, request

from data import YT_Data

app = Flask(__name__, template_folder="../templates", static_folder="../static")
api = YT_Data()

@app.route("/")
def home():
    response = api.search("3Blue1Brown")
    return render_template("home.html", search_response=response)

@app.route("/watch")
def player():
    query = request.args.get('play')
    is_playlist = request.args.get('playlist', 'false').lower()
    index = int(request.args.get('index', '1'))
    
    if is_playlist == 'true':
        is_playlist = True
        api.fetch_playlist(query, indexc)
    else:
        is_playlist = False
        response = api.fetch_video(query)
        
    response = response[0]

    return render_template("player.html", query=query, video=response, playlist=is_playlist)

# for testing and rewriting index folder: 
@app.route("/index")
def index():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)