from flask import Flask, jsonify

app = Flask(__name__)

data={"x":100, "y":200, "z":300}

@app.route('/')
def index():
    return "<h1>Hello world</h1>"

@app.route('/data', methods=["GET"])
def get_data():
    return jsonify(data),200

@app.route('/data', methods=['POST'])
def insert_data():
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)