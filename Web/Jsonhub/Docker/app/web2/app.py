from flask import Flask, request, render_template_string, abort
import re
import json
import string, random

app = Flask(__name__)


def log():
    if request.method == "GET":
        s = "GET {}".format(request.url)

    elif request.method == "POST":
        s = "POST {}\n{}".format(request.url, request.data)
    else:
        s = "Error! {}".format(request.method)
    with open("/var/tmp/flask.log", "wb") as log:
        log.write(s.encode("utf8"))
        log.write(b"\n")


@app.before_request
def before_request():
    data = str(request.data)
    log()
    if "{{" in data or "}}" in data or "{%" in data or "%}" in data:
        abort(401)


@app.route('/')
def index():
    return "flag{" + ''.join(random.choices(string.ascii_letters + string.digits, k=32)) + "}"


@app.route('/admin')
def whoami():
    return __import__("os").popen("whoami").read()


@app.route('/caculator', methods=["POST"])
def caculator():
    try:
        data = request.get_json()
    except ValueError:
        return json.dumps({"code": -1, "message": "Request data can't be unmarshal"})
    num1 = str(data["num1"])
    num2 = str(data["num2"])
    symbols = data["symbols"]
    if re.search("[a-z]", num1, re.I) or re.search("[a-z]", num2, re.I) or not re.search("[+\-*/]", symbols):
        return json.dumps({"code": -1, "message": "?"})

    return render_template_string(str(num1) + symbols + str(num2) + "=" + "?")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
