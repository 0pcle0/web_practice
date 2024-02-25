from flask import Flask, request, redirect, render_template
from datetime import datetime
import pymysql

app = Flask(__name__)

writ = [
    {'id':1, 'title':'안녕하세요1', 'body':'반갑습니다1', 'user':'사용자1', 'date':'2024.01.24'},
    {'id':2, 'title':'안녕하세요2', 'body':'반갑습니다2', 'user':'사용자2', 'date':'2024.02.24'},
    {'id':3, 'title':'안녕하세요3', 'body':'반갑습니다3', 'user':'사용자3', 'date':'2024.03.24'},
    {'id':4, 'title':'안녕하세요4', 'body':'반갑습니다4', 'user':'사용자4', 'date':'2024.04.24'}
    ]


db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     passwd='noneage0522!',
                     db='notice',
                     charset='utf8')

with db.cursor() as cur:
    sql = ''' CREATE TABLE NOTICE1(
              ID INT NOT NULL,
              TITLE CHAR(40) NOT NULL,
              BODY CHAR(255) NOT NULL,
              USER CHAR(15) NOT NULL,
              DATE CHAR(40) NOT NULL,
              PRIMARY KEY(ID)
              )ENGINE=INNODB;'''
    
    cur.execute(sql)
    db.commit()


sql = '''INSERT INTO notice1 (id, title, body, user, date) VALUES (%s, %s, %s, %s, %s)'''


with db.cursor() as cur:
    for arti in writ:
        sql = '''INSERT INTO notice1 (id, title, body, user, date) VALUES (%s, %s, %s, %s, %s)'''
        cur.execute(sql,(arti['id'], arti['title'], arti['body'],arti['user'], arti['date']))
        db.commit()



word1 ='%'+'안녕'+'%'
cur = db.cursor()
sql = '''SELECT * FROM notice1 WHERE title LIKE %s or body LIKE %s '''
cur.execute(sql,(word1,word1))
records = cur.fetchall()    
relist = []
for arti in records:
    reDict = {
        'id':arti[0],
        'title':arti[1],
        'body':arti[2],
        'user':arti[3],
        'date':arti[4]
        }
    relist.append(reDict)
    db.commit

print(relist)
