from flask import Flask
from flask import redirect
from flask import request

import hashlib
import json
import os
import random
import glob
import re
import shutil

PIdWhiteList = ["Register"]
app = Flask(__name__)


@app.route('/')
def index():
  hoge = glob.glob("pg/*/")
  docslist = []
  for i in hoge:
    title = open(i + "Title.txt", "r", encoding="utf-8").read()
    docslist.append(
      re.sub(r"pg/([0-9a-zA-Z]*)/",
             r"<a class='btn btn-flat' href=page/\1>" + title + r"</a>", i))

  hoge = glob.glob("pgbot/*/")
  docslistb = []
  for i2 in hoge:
    title = open(i2 + "Title.txt", "r", encoding="utf-8").read()
    docslistb.append(
      re.sub(r"pgbot/([0-9a-zA-Z]*)/",
             r"<a class='btn btn-flat' href=page/\1>" + title + r"</a>", i2))
  return open("index.html", "r", encoding="utf-8").read().replace(
    "<!-- DocsListA -->", "<br>\n".join(docslist),
    1).replace("<!-- DocsListB -->", "<br>\n".join(docslistb), 1)


@app.route('/page/<ids>')
def page(ids):
  try:
    text = open(f"pg/{ids}/Docs.txt", "r", encoding="utf-8").read()
    name = open(f"pg/{ids}/name.txt", "r", encoding="utf-8").read()
    title = open(f"pg/{ids}/Title.txt", "r", encoding="utf-8").read()
    comment = open(f"pg/{ids}/comment.txt", "r", encoding="utf-8").read()
    basic = open("basic.html", "r", encoding="utf-8").read()
    basic = basic.replace("{BEBN}", name, 1)
    basic = basic.replace("{BEB2}", title, 3)
    basic = basic.replace("{$COMMENT}", comment, 1)
    basic = basic.replace("{DCODE}", ids)
    basic = basic.replace("{BEB1}", text, 1)

    return basic
  except FileNotFoundError:
    try:
      text = open(f"pgbot/{ids}/Docs.txt", "r", encoding="utf-8").read()
      name = open(f"pgbot/{ids}/name.txt", "r", encoding="utf-8").read()
      title = open(f"pgbot/{ids}/Title.txt", "r", encoding="utf-8").read()
      comment = open(f"pgbot/{ids}/comment.txt", "r", encoding="utf-8").read()

      basic = open("basic.html", "r", encoding="utf-8").read()
      basic = basic.replace("{BEBN}", name, 1)
      basic = basic.replace("{BEB2}", title, 3)
      basic = basic.replace("{$COMMENT}", comment, 1)
      basic = basic.replace("{DCODE}", ids)
      basic = basic.replace("{BEB1}", text, 1)

      return basic
    except FileNotFoundError:
      return "そんな記事あったか？"


@app.route("/Create/")
def createpage():
  return open("make.html", "r", encoding="utf-8").read()


@app.route("/cr", methods=["POST", "GET"])
def creates():
  if request.form.get("text") == "" or request.form.get("title") == "":
    return "Invalid Text or Title"
  hoge = glob.glob("pg/*/")
  users = json.load(open("user.json", "r", encoding="utf-8"))
  if request.form.get("uc") != "" and request.form.get("uc") in list(
      users.keys()):
    while True:
      ids = "".join([
        random.choice(
          "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
        for i in range(14)
      ])
      if not ids in hoge:
        break
    print(users)
    os.makedirs(f"pg/{ids}")
    open(f"pg/{ids}/Docs.txt", "w", encoding="utf-8").write(
      request.form.get("text").replace("\n", "<br>"))
    open(f"pg/{ids}/name.txt", "w",
         encoding="utf-8").write(users[request.form.get("uc")][0])
    open(f"pg/{ids}/Title.txt", "w",
         encoding="utf-8").write(request.form.get("title"))
    open(f"pg/{ids}/comment.txt", "w", encoding="utf-8")
    open(f"pg/{ids}/count.txt", "w", encoding="utf-8").write("0")
    
    return redirect("/")
  else:
    return "無効なユーザーコード"


@app.route("/bot/cr", methods=["POST", "GET"])
def creates2():
  if request.form.get("text") == "" or request.form.get("title") == "":
    return "Invalid Text or Title"
  hoge = glob.glob("pgbot/*/")
  users = json.load(open("user.json", "r", encoding="utf-8"))
  if request.form.get("uc") != "" and request.form.get("uc") in list(
      users.keys()):
    while True:
      ids = "".join([
        random.choice(
          "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
        for i in range(14)
      ])
      if not ids in hoge:
        break
    print(users)
    os.makedirs(f"pgbot/{ids}")
    open(f"pgbot/{ids}/Docs.txt", "w", encoding="utf-8").write(
      request.form.get("text").replace("\n", "<br>"))
    open(f"pgbot/{ids}/name.txt", "w",
         encoding="utf-8").write(users[request.form.get("uc")][0])
    open(f"pgbot/{ids}/Title.txt", "w",
         encoding="utf-8").write(request.form.get("title"))
    open(f"pgbot/{ids}/comment.txt", "w", encoding="utf-8")
    open(f"pgbot/{ids}/count.txt", "w", encoding="utf-8").write("0")

    return redirect("/")
  else:
    return "無効なユーザーコード"


@app.route("/report")
def rep():
  a = json.load(open("rep.json", "r", encoding="utf-8"))
  PId = request.args.get("p")
  if PId in a.keys():
    if PId in PIdWhiteList:
      return "<h1>意味のない報告だよ</h1>"
    a[PId] += 1
  else:
    a[PId] = 1
  if a[PId] >= 20 and a[PId] < 30:
    try:
      mes = open("deleteMessage", "r", encoding="utf-8")
      open(f'pg/{PId}/Docs.txt', "w").write(mes.read())
    except:
      open(f'pgbot/{PId}/Docs.txt', "w").write("""<h1>あぼーん</h1>
<p>いっぱい報告されてるため記事の内容は消去されました</p>""")
  if a[PId] > 30:
    try:
      shutil.rmtree(f'pg/{PId}/')
    except:
      shutil.rmtree(f'pgbot/{PId}/')

  json.dump(a, open("rep.json", "w", encoding="utf-8"), indent=4)
  return redirect("/")


@app.route("/reg", methods=["POST", "GET"])
def register():
  print(request.form.get("name"))
  users = json.load(open("user.json", "r", encoding="utf-8"))
  while True:
    ids = "".join([
      random.choice("1234567890abcdefghijklmnopqrstuvwxyz+$") for i in range(7)
    ])
    if not ids in list(users.keys()):
      break
  users[ids] = [request.form.get("name"), request.form.get("Mail")]
  json.dump(users, open("user.json", "w", encoding="utf-8"), indent=4)
  return "メモしておいてね。<br>ユーザーコード:" + ids


@app.route("/comment", methods=["get", "post"])
def com1():
  users = json.load(open("user.json", "r", encoding="utf-8"))
  kcode = request.form.get("code")
  usec = request.form.get("uc")
  usn = users[usec][0]
  txt = request.form.get("text")
  txt = txt.replace(">", "≻")
  txt = txt.replace("<", "≺")
  txt = txt.replace("\n", "<br>\n")
  ids = hashlib.md5(request.remote_addr.encode()).hexdigest()
  try:
    c = int(open(f"pg/{kcode}/count.txt", "r").read())+1
    open(f"pg/{kcode}/count.txt", "w").write(str(c))
    f = open(f"pg/{kcode}/comment.txt", "a")
    f.write(f"<br>{c}:<font color='green'><b>{usn}</b></font> ID:{ids}<br>")
    f.write(txt)
    f.write("\n\n<br><br>\n\n\n")
      
  except FileNotFoundError:
    try:
      c = int(open(f"pgbot/{kcode}/count.txt", "r").read())+1
      open(f"pgbot/{kcode}/count.txt", "w").write(str(c))
      f = open(f"pgbot/{kcode}/comment.txt", "a")
      f.write(f"<br>{c}:<font color='green'><b>{usn}</b></font> ID:{ids}<br>")
      f.write(txt)
      f.write("\n\n<br><br>\n\n\n")
    except:
      return "Invalid PageID"
  return redirect(f"/page/{kcode}")

@app.route("/API.txt")
def robot():
  return json.load(open("API.json", "r", encoding = "utf-8"))

app.run(host='0.0.0.0', port=8000, debug=True)
