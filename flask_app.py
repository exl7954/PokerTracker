from flask import Flask
from flask import request
from MakeLedger import makeLedger
app = Flask(__name__)

@app.route("/")
def index():
    return """<html>
    <head>
        <title>Eric Ledger</title>
    </head>
    <body>
    <h1>Enter PokerNow link:</h1>
    <form action="/ledger" id="in">
    <input type="text" id="url">
    <button form="in" type="submit">Go</button>
    </form>
    </body>
    </html>"""

@app.route("/ledger")
def ledger():
    url = request.args.get("url")
    return makeLedger(url)

if __name__ == '__main__':
    app.run()