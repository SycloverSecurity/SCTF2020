from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=["POST","GET"])
def security():
    secret = request.form["cmd"]
    for i in secret:
        if not 42 <= ord(i) <= 122: return "error!"

    exec(secret)
    return "xXXxXXx"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
