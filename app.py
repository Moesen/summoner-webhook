from flask import Flask, render_template
from core.DataCollectionStrategy.tasks import get_stats_for_all


app = Flask(__name__, template_folder="core/DataCollectionStrategy/templates")

@app.route("/")
def index():
    stats = get_stats_for_all()
    print()
    return render_template("index.html", stats = stats)

if __name__ == "__main__":
    app.debug = True
    app.run()