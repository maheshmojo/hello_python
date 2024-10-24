from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello')
def hello():
    return jsonify(message="Hello, World!")

@app.route('/greet')
def greet():
    return jsonify(message="Greetings, World!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
