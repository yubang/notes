#coding:UTF-8

from flask import Blueprint,render_template,g,request,redirect,url_for,session
from functools import wraps
from models import sessionMaker,AccountModel
import hashlib


notesApp=Blueprint("notes",__name__)


def checkUser(fn):
    "检测用户是否登录"
    @wraps(fn)
    def deal(*args,**kwds):
        if session.has_key("uid"):
            return fn(*args,**kwds)
        else:
            return redirect("/notes/account/login")
        
    return deal


@notesApp.route("/")
@checkUser
def index():
    "日程主界面"
    return render_template("notes/index.html")


@notesApp.route("/getNotes")
@checkUser   
def getNotes():
    "获取日程"
    g.lists=[1]
    return render_template("notes/notes.html")


@notesApp.route("/account/<requestType>",methods=['GET','POST'])    
def account(requestType):
    "用户帐号模块"
    
    g.message = request.args.get("error","")
    
    if requestType == "login":
        #登录
        if request.method == "GET":
            g.title = u"登录"
            g.login = True
            return render_template("notes/account.html")
        else:
            username=request.form.get("username",None)
            password = request.form.get("password","")
            password = hashlib.md5(password).hexdigest()
            
            dbSession = sessionMaker()
            query=dbSession.query(AccountModel)
            obj=query.filter(username == username).first()
            dbSession.close()
            
            if obj == None:
                #用户名不存在
                return redirect(u"/notes/account/login?error=用户名不存在")
            else:
                if obj.password == password:
                    #登录成功
                    session['uid'] = obj.id
                    return redirect(url_for("notes.index"))
                else:
                    #密码错误
                    return redirect(u"/notes/account/login?error=密码错误")
            
            
    else:
        if request.method == "GET":
            g.login = False
            g.title = u"注册"
            return render_template("notes/account.html")
        else:
            username=request.form.get("username",None)
            password = request.form.get("password","")
            password = hashlib.md5(password).hexdigest()
            
            dbSession=sessionMaker()
            dao=AccountModel(username,password)
            dbSession.add(dao)
            try:
                dbSession.commit()
                result=True
            except:
                dbSession.rollback()
                result=False
            
            dbSession.close()
            
            if result :
                session['uid']=dao.id
                return redirect(url_for("notes.index"))
            else:
                return redirect(u"/notes/account/register?error=用户名已经被注册")


@notesApp.route("/accountExit")
@checkUser                
def exitAccount():
    "退出登录"
    del session['uid']
    return redirect(url_for("notes.index"))                
