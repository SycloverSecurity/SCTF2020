from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Token
from .utils import ssrf_check
import json
import requests
import base64


def login(request):
    if request.method == "GET":
        return render(request, "templates/login.html")
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({"code": -1, "message": "Request data can't be unmarshal"})
        user = auth.authenticate(**data)
        if user is not None:
            auth.login(request, user)
            return JsonResponse({"code": 0})
        else:
            return JsonResponse({"code": 1})


def reg(request):
    if request.method == "GET":
        return render(request, "templates/reg.html")
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({"code": -1, "message": "Request data can't be unmarshal"})

        if len(User.objects.filter(username=data["username"])) != 0:
            return JsonResponse({"code": 1})
        User.objects.create_user(**data)
        return JsonResponse({"code": 0})


@login_required
def home(request):
    if request.method == "GET":
        return render(request, "templates/home.html")
    elif request.method == "POST":
        white_list = ["10.227.6.31:10000"]
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({"code": -1, "message": "Request data can't be unmarshal"})

        if Token.objects.all().first().Token == data["token"]:
            try:
                if ssrf_check(data["url"], white_list):
                    return JsonResponse({"code": -1, "message": "Hacker!"})
                else:
                    res = requests.get(data["url"], timeout=1)
            except Exception:
                return JsonResponse({"code": -1, "message": "Request Error"})
            if res.status_code == 200:
                return JsonResponse({"code": 0, "message": res.text})
            else:
                return JsonResponse({"code": -1, "message": "Something Wrong"})
        else:
            return JsonResponse({"code": -1, "message": "Token Error"})


def flask_rpc(request):
    if request.META['REMOTE_ADDR'] != "127.0.0.1":
        return JsonResponse({"code": -1, "message": "Must 127.0.0.1"})

    methods = request.GET.get("methods")
    url = request.GET.get("url")

    if methods == "GET":
        return JsonResponse(
            {"code": 0, "message": requests.get(url, headers={"User-Agent": "Django proxy =v="}, timeout=1).text})
    elif methods == "POST":
        data = base64.b64decode(request.GET.get("data"))
        return JsonResponse({"code": 0, "message": requests.post(url, data=data,
                                                                 headers={"User-Agent": "Django proxy =v=",
                                                                          "Content-Type": "application/json"}, timeout=1).text})
    else:
        return JsonResponse({"code": -1, "message": "=3="})
