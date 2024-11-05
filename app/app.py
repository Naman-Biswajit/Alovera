from flask import Flask
from flask import render_template, request


app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/watch")
def video_player():
    query = request.args.get('play')
    return render_template("player.html", query=query)

if __name__ == "__main__":
    app.run(debug=True)