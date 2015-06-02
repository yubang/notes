#coding:UTF-8

from flask import Blueprint,render_template,g,request,redirect,url_for,session
from functools import wraps
from models import sessionMaker,AccountModel,MessageModel
import hashlib,datetime


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


def dealMessage(obj):
    "处理日程类"
    d=obj.remindDate-datetime.date.today()
    obj.date=d.days
    if obj.date == 0:
        obj.date = u"今"
    return obj

@notesApp.route("/")
@checkUser
def index():
    "日程主界面"
    return render_template("notes/index.html")


@notesApp.route("/getNotes")
@checkUser   
def getNotes():
    "获取日程"
    print session
    dbSession=sessionMaker()
    query=dbSession.query(MessageModel)
    lists=query.filter(MessageModel.uid == session['uid'],MessageModel.status == 0,MessageModel.remindDate >= datetime.date.today()).order_by("remindDate,id").all()
    dbSession.close()
    
    g.lists=map(dealMessage,lists)
    
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
            obj=query.filter(AccountModel.username == username).first()
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
                session['uid']=dao.id
                result=True
            except:
                dbSession.rollback()
                result=False
            
            dbSession.close()
            
            if result :
                return redirect(url_for("notes.index"))
            else:
                return redirect(u"/notes/account/register?error=用户名已经被注册")


@notesApp.route("/accountExit")
@checkUser                
def exitAccount():
    "退出登录"
    del session['uid']
    return redirect(url_for("notes.index"))
    

@notesApp.route("/manageUi")
@checkUser
def manageUi():
    "后台管理界面"
    return render_template("notes/manageUi.html")

@notesApp.route("/add",methods=['GET','POST'])
@checkUser    
def add():
    "添加日程"
    if request.method == "GET":
        g.title = u"添加日程"
        g.submit = u"添加"
        return render_template("notes/edit.html")
    else:
        remindDate=request.form.get("remindDate",None)
        message=request.form.get("message",None)
        uid=session.get("uid",None)
        dao=MessageModel(uid,message,remindDate)
        dbSession=sessionMaker()
        dbSession.add(dao)
        try:
            dbSession.commit()
            r=True
        except:
            dbSession.rollback()
            r=False
        finally:
            dbSession.close()
        return redirect(url_for("notes.index"))
        

@notesApp.route("/notesManager")
@checkUser
def notesManager():
    "日程管理"
    dbSession=sessionMaker()
    query=dbSession.query(MessageModel)
    g.lists=query.filter(MessageModel.status != -1,MessageModel.uid == session['uid']).all()
    dbSession.close()
    return render_template("notes/notesManager.html")
    
    
@notesApp.route("/edit",methods=['GET','POST'])
def edit():
    if request.method == "GET":
        g.title = u"修改日程"
        g.submit = u"修改"
        
        id=request.args.get("id","")
        
        dbSession=sessionMaker()
        obj=dbSession.query(MessageModel).filter(MessageModel.id == id,MessageModel.uid == session['uid']).one()
        dbSession.close()
        
        g.remindDate = obj.remindDate.strftime("%Y-%m-%d")
        g.message = obj.message
        
        return render_template("notes/edit.html")
    else:
        id=request.args.get("id",None)
        remindDate = request.form.get("remindDate",None)
        message = request.form.get("message",None)
        
        dbSession = sessionMaker()
        dbSession.query(MessageModel).filter(MessageModel.uid == session['uid'],MessageModel.id == id).update({"remindDate":remindDate,"message":message})
        dbSession.commit()
        dbSession.close()
        
        return redirect(url_for("notes.notesManager"))


@notesApp.route("/delete")
@checkUser    
def delete():
    "删除日程"
    id=request.args.get("id","")
    dbSession=sessionMaker()
    dbSession.query(MessageModel).filter(MessageModel.uid == session['uid'],MessageModel.id == id).update({"status":-1})
    dbSession.commit()
    dbSession.close()
    return redirect(url_for("notes.notesManager"))
