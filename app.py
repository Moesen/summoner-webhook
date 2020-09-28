from flask import Flask, render_template
import json

app = Flask(__name__, template_folder="core/DataExportStrategy/Flask/templates", static_folder="core/DataExportStrategy/Flask/static")

@app.route("/")
def index():
    summoners_stats = json.loads(open("core/DataStoringStrategy/summoners_data.json", "r").read())
    return render_template("index.html", summoners_stats=summoners_stats)

if __name__ == "__main__":
    app.debug = True
    app.run()