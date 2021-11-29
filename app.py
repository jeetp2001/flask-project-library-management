from flask import Flask,request
from flask.templating import render_template
import mysql.connector
from datetime import date

con = mysql.connector.connect(host='localhost',user='root',password='G0d!sgreat',database='flaskproject3')
cur = con.cursor()

app = Flask(__name__)

@app.route('/',methods = ['GET', 'POST'])
def fun1():
    q12 = 'select student_id from books_issued group by student_id'
    cur.execute(q12)
    data12 = cur.fetchall()
    l12 = []
    for i in data12:
        l12.append(i[0])
    for i in l12:
        q13 = 'select date,copies from books_issued where student_id=%s and copies != %s'
        t13 = (i,0)
        cur.execute(q13,t13)
        data13 = cur.fetchall()
        f = 0
        for j in data13:
            n = (date.today() - j[0]).days
            q = n//7
            s = 500 * q * j[1]
            f = f + s
        q14 = 'select * from fine'
        cur.execute(q14)
        data14 = cur.fetchall()
        for k in data14:
            if k[0]==i:
                q15 = 'update fine set fine=%s where student_id=%s'
                t15 = (f,i)
                cur.execute(q15,t15)
                con.commit()
                break
        else:
            q16 = 'insert into fine values (%s,%s)'
            t16 = (i,f)
            cur.execute(q16,t16)
            con.commit()
    return render_template('login.html')
        
@app.route('/home',methods=['GET','POST'])
def fun2():
    if request.form.get('sid') == '':
        return render_template('error.html')
    else:
        sid = int(request.form.get('sid'))
        spwd = str(request.form.get('spwd'))
        q = 'select * from login'
        cur.execute(q)
        data1 = cur.fetchall()
        d1 = {}
        q2 = 'select * from books'
        cur.execute(q2)
        data2 = cur.fetchall()
        q3 = 'select * from books_issued where copies != %s order by student_id,date'
        t3 = (0,)
        cur.execute(q3,t3)
        data3 = cur.fetchall()
        q17 = 'select * from fine where fine != 0'
        cur.execute(q17)
        data17 = cur.fetchall()
        d2 = {}
        d3 = {}
        for i in data2:
            d2[i[1]]=i[2]
        for i in data1:
            d1[i[1]]=i[2]
        if sid in d1.keys():
            if d1[sid] == spwd:
                if sid == 1:
                    return render_template('adminhome.html',output_data=data3,output_data2=data2,output_date3=data17)
                else:
                    return render_template('home.html',output_data=data2,output_data2=sid)
            else:
                return render_template('spwderror.html')
        else:
            return render_template('siderror.html')

@app.route('/issue/<name>/<sid>/<author>')
def fun3(name,sid,author):
    q1 = "select  student_id,title,date from books_issued"
    cur.execute(q1)
    data1 = cur.fetchall()
    date_today = date.today()
    q6 = 'select copies from books where title=%s'
    t6 = (name,)
    cur.execute(q6,t6)
    data6 = cur.fetchall()
    if data6[0][0] > 0:
        for i in data1:
            if i[0]==int(sid) and i[1]==name and i[2]==date_today:
                q11 = "select copies from books_issued where student_id=%s and title=%s"
                t11 = (sid,name)
                cur.execute(q11,t11)
                data11 = cur.fetchall()
                q22 = "update books_issued set copies=%s where student_id=%s and title=%s"
                t22 = (data11[0][0]+1,sid,name)
                cur.execute(q22,t22)
                con.commit()
                break
        else:    
            q2 = 'insert into books_issued values (%s,%s,%s,%s,%s)'
            t2=(sid,name,author,1,date_today)
            cur.execute(q2,t2)
            con.commit()
        q4 = 'select copies from books where title=%s' 
        t4 = (name,)
        cur.execute(q4,t4)
        data4 = cur.fetchall()
        q5 = 'update books set copies=%s where title=%s'
        t5=(data4[0][0]-1,name)
        cur.execute(q5,t5)
        con.commit()
        return render_template('issued.html',data=name)
    else:
        return render_template('unavailable.html')

@app.route('/return/<sid>')
def fun4(sid):
    q7 = "select  * from books_issued where student_id=%s and copies != %s"
    t7=(sid,0)
    cur.execute(q7,t7)
    data7 = cur.fetchall()
    if not len(data7):
        return render_template('return2.html')
    else:
        return render_template('return.html',output_data=data7,output_data2=sid)

@app.route('/returned/<name>/<sid>/<date_today>')
def fun5(name,sid,date_today):
    q9 = "select copies from books where title=%s"
    t9 = (name,)
    cur.execute(q9,t9)
    data9 = cur.fetchall()
    q8 = "update books set copies=%s where title=%s"
    t8 = (data9[0][0]+1,name)
    cur.execute(q8,t8)
    con.commit()
    q10 = "select copies from books_issued where title=%s and student_id=%s and date=%s"
    t10 = (name,sid,date_today)
    cur.execute(q10,t10)
    data10 = cur.fetchall()
    q11 = "update books_issued set copies=%s where title=%s and student_id=%s"
    t11 = (data10[0][0]-1,name,sid)
    cur.execute(q11,t11)
    con.commit()
    return render_template('returned.html')

if __name__ == '__main__':
    app.run()
