import flask
import harambot
app = flask.Flask(__name__)

@app.route("/")
def index():
    #do whatevr here...
    harambot.main()
