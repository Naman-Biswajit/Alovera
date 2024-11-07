from flask import Flask
from flask import render_template, request

from data import YT_Data

app = Flask(__name__, template_folder="../templates", static_folder="../static")
api = YT_Data()

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/watch")
def video_player():
    query = request.args.get('play')
    response = api.fetch_video(query)[0]
    return render_template("player.html", query=query, video=response)

if __name__ == "__main__":
    app.run(debug=True)