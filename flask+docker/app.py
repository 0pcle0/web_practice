from flask import Flask, request, redirect, render_template
from datetime import datetime
import pymysql

app = Flask(__name__)



newID = 5
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



@app.route('/')
def webf():
    return render_template('main.html', writ = writ)



@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    date =''
    for arti in writ:
        if id == arti['id']:
            title = str(arti['title'])
            body = str(arti['body'])
            date = arti['date']
            break;
    return render_template('read.html', id=id, title=title, body=body, date=date)


@app.route('/create/', methods=['GET','POST'])
def create():
    if request.method =='GET':
        return render_template('create.html')
    
    elif request.method == 'POST':
        global newID
        title = str(request.form['title'])
        body = str(request.form['body'])
        user = '사용자'+str(newID)
        date = datetime.now()
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
        newwri = {'id':newID, 'title':title, 'body':body, 'user':user, 'date':date}
        url = '/read/'+str(newID)+'/'
        with db.cursor() as cur:
            sql = '''INSERT INTO notice1 (id, title, body, user, date) VALUES (%s, %s, %s, %s, %s)'''
            cur.execute(sql,(newwri['id'],newwri['title'], newwri['body'], newwri['user'], newwri['date']))
            db.commit()
        newID += 1
        writ.append(newwri)
        return redirect(url)


@app.route('/update/<int:id>/', methods=['GET','POST'])
def update(id):
    if request.method =='GET':
        title = ''
        body = ''
        for arti in writ:
            if id == arti['id']:
                title = arti['title']
                body = arti['body']
                date = arti['date']
                break
        return render_template('update.html', id=id, title=title, body=body, date=date)
    
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        for arti in writ:
            if id == arti['id']:
                arti['title']=title
                arti['body']=body
                date = datetime.now()
                date = date.strftime("%Y/%m/%d, %H:%M:%S")
                arti['date']=date
                break;
        with db.cursor() as cur:
            sql = '''UPDATE notice1 SET title=%s, body=%s, date=%s WHERE ID=%s'''
            cur.execute(sql,(title, body, date,arti['id']))
            db.commit()
        url = '/read/'+str(id)+'/'
        return redirect(url)


@app.route('/search/', methods=['POST'])
def search():
    if request.method == 'POST':
        searchtype = request.form['searchtype']
        search = request.form['search']
        word1 = '%'+request.form['search']+'%'
        if searchtype == 'title':
            cur = db.cursor()
            sql = '''SELECT * FROM notice1 WHERE title LIKE %s'''
            cur.execute(sql,(word1))
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
            return render_template('search.html', searchtype=searchtype, search=search, relist=relist)

        elif searchtype == 'body':
            cur = db.cursor()
            sql = '''SELECT * FROM notice1 WHERE body LIKE %s'''
            cur.execute(sql,(word1))
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
            return render_template('search.html', searchtype=searchtype, search=search, relist=relist)
        
        elif searchtype == 'titlebody':
            cur = db.cursor()
            sql = '''SELECT * FROM notice1 WHERE title LIKE %s or body LIKE %s'''
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
            return render_template('search.html', searchtype=searchtype, search=search, relist=relist)



@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for arti in writ:
        if id == arti['id']:
            writ.remove(arti)
            break
    with db.cursor() as cur:
            sql = '''DELETE FROM notice1 WHERE ID=%s'''
            cur.execute(sql,(arti['id']))
            db.commit()
    return redirect('/')


if __name__=="__main__":
    app.run(port=5003)
