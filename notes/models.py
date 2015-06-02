#coding:UTF-8

"""
数据库模型类
"""

from sqlalchemy import create_engine,Table,MetaData,Column
from sqlalchemy.sql.sqltypes import String,Integer,TIMESTAMP
from sqlalchemy.orm import mapper,sessionmaker

import config

db = create_engine("mysql://%s:%s@%s:%d/%s"%(config.MYSQL_USER,config.MYSQL_PASSWORD,config.MYSQL_HOST,config.MYSQL_PORT,config.MYSQL_DB))

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
        
mapper(AccountModel,accountTable)
sessionMaker=sessionmaker(bind=db)
