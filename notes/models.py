#coding:UTF-8

"""
数据库模型类
"""

from sqlalchemy import create_engine,Table,MetaData,Column
from sqlalchemy.sql.sqltypes import String,Integer,TIMESTAMP,DATE
from sqlalchemy.orm import mapper,sessionmaker

import config
import time

db = create_engine("mysql://%s:%s@%s:%d/%s?charset=UTF8"%(config.MYSQL_USER,config.MYSQL_PASSWORD,config.MYSQL_HOST,config.MYSQL_PORT,config.MYSQL_DB),echo=True)

accountTable = Table('notes_account',MetaData(db),
    Column('id',Integer,primary_key=True),
    Column('username',String(30),unique=True),
    Column('password',String(30)),
    Column('createTime',TIMESTAMP),
)

class AccountModel(object):
    "帐号类"
    def __init__(self,username,password):
        self.username=username
        self.password=password


messageTable = Table('notes_message',MetaData(db),
    Column('id',Integer,primary_key=True),
    Column('uid',Integer),
    Column('message',String(200)),
    Column('remindDate',DATE),
    Column('status',Integer),
    Column('updateTime',TIMESTAMP),
)

class MessageModel(object):
    "日程类"
    def __init__(self,uid,message,remindDate):
        self.uid=uid
        self.message=message
        self.remindDate=remindDate
        self.status = 0
        self.updateTime=time.strftime("%Y-%m-%d %H:%M:%S")
        
mapper(AccountModel,accountTable)
mapper(MessageModel,messageTable)
sessionMaker=sessionmaker(bind=db)
