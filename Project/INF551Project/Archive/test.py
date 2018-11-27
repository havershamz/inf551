import json

from bottle import route, run, template, request, redirect


@route('/index')
def index():
    data = "None"

    return template("index.html", data=data)


@route('/index', method="POST")
def process():
    print(request)
    data = request.forms.get('kwd')
    print(data)

    return template("index.html", data=data)

# @route('/hello/<kwd>')
# def index(kwd):
#
#     # firebase
#
#     musics = [{"name": "test"}]
#
#     data = []
#     for music in musics:
#         if kwd in music['name']:
#             data.append(music)
#     print(data)
#     return template("index.html", data=data)


run(host='localhost', port=8080)