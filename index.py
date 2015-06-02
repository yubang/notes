#coding:UTF-8

"""
一个日程管理小工具
@author:yubang
2015-05-31
"""

from flask import Flask,redirect
from notes.app import notesApp
import config

app=Flask(__name__)
app.secret_key = config.secret_key
app.register_blueprint(notesApp,url_prefix="/notes")

@app.route("/")
def index():
    "主页"
    return redirect("/notes/")

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)
