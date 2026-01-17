from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=["GET"])
def success():
    return ({
        "message": "Backend radi!"
    })

if __name__ == "__main__":
    app.run(debug=True)