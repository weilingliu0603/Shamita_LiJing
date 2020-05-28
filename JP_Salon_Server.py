import sqlite3
import flask

app = flask.Flask(__name__)

def get_db():
    db= sqlite3.connect('jpsalon2.db')
    db.row_factory= sqlite3.Row
    return db


@app.route('/')

def home():
    return flask.render_template('indexnew.html')


@app.route('/newsdetails')

def newsdetails():
    return flask.render_template('news.html')
    

@app.route('/add_member')
def add_member():
    db= get_db()
    rows= db.execute('SELECT seq FROM sqlite_sequence WHERE name="member"')
    for line in rows:
        ID= line['seq']
    ID +=1
    db.close()
    return flask.render_template('add_new_member.html',ID=ID)

@app.route('/added', methods=['POST'])

def added():
    ID=flask.request.form['memberID']
    name=flask.request.form['fullName']
    g=flask.request.form['gender']
    email=flask.request.form['email']
    num=flask.request.form['contactNo']
    address=flask.request.form['address']
    db=get_db()
    db.execute('INSERT into member(memberID,name,gender,email,contactNumber,address) VALUES(?,?,?,?,?,?)',(int(ID),name,g,email,num,address))
    db.commit()
    db.close()
    return flask.render_template('memberadded.html',n=name)


 
@app.route('/add_new_transaction')
def add_new_transaction():
    invoice=0
    db = get_db()
    rows= db.execute('SELECT seq FROM sqlite_sequence WHERE name="Invoice"')
    for line in rows:
        invoice= line['seq']
    invoice+=1
    return flask.render_template('add_new_transaction.html',invoice=invoice)


@app.route('/added2', methods=['POST'])

def added2():
    invoicen=flask.request.form['invoiceNo']
    ID=flask.request.form['memberID']
    date=flask.request.form['date']
    name=flask.request.form['name']
    serviceID=flask.request.form['serviceID']
    amount=flask.request.form['totalAmount']
    db= get_db()
    db.execute('INSERT into Invoice(invoiceNo,memberID,date,name,totalAmount) VALUES(?,?,?,?,?)',(int(invoicen),int(ID),date,name,float(amount)))
    db.execute('INSERT into Invoice_detail(invoiceNo,ServiceID) VALUES(?,?)',(int(invoicen),serviceID))
    db.commit()
    db.close()
    return flask.render_template('transactionadded.html', n=invoicen)
    
       

    



@app.route('/daily_transaction')

def view_daily_transaction():
    return flask.render_template('daily_transaction.html')

@app.route('/viewed_d_t', methods=['POST'])

def viewed_d_t():
    db=get_db()
    rows=db.execute("SELECT * FROM Invoice WHERE date=?",[flask.request.form['date']]).fetchall()
    db.close()
    return flask.render_template('view_d_t.html',rows=rows)
    



@app.route('/monthly_revenue')

def view_monthly_revenue():
    return flask.render_template('monthly_revenue.html')



@app.route('/viewed_m_r', methods=['POST'])


def viewed_m_r():
    db=get_db()
    result=0.0
    sd=flask.request.form["startdate"]
    ed=flask.request.form=["enddate"]
    rows=db.execute("SELECT totalAmount FROM Invoice WHERE date>=(?) AND date<=(?)",(str(sd),str(ed))).fetchall()
    print(rows)
    print("--------------------------")
    for i in rows:
        result+= i['totalAmount']
    print(result)
    print("----------------------------")
    
    return flask.render_template('view_m_r.html',result=result)

@app.route('/member_transaction')

def view_member_transaction():
    return flask.render_template('member_transaction.html')



@app.route('/viewed_m_t',methods=['POST'])

def viewed_m_t():
    db=get_db()
    mem_id=flask.request.form["memberID"]
    m_id=int(mem_id)
    rows=db.execute("SELECT * FROM Invoice,Invoice_detail WHERE Invoice.memberID=(?) AND Invoice_detail.invoiceNo=Invoice.invoiceNo",(m_id,)).fetchall()
    return flask.render_template('view_m_t.html',rows=rows)





@app.route("/update_address")
def update_address():
    return flask.render_template('update_address.html')

@app.route("/updated_address",methods=["POST"])
def updated_address():#update the new address
    address=flask.request.form["address"]
    ID=flask.request.form["memberID"]
    db=get_db()
    db.execute("UPDATE member SET address=(?) WHERE memberID=(?)",(address,int(ID)))
    db.commit()
    db.close()
    return flask.render_template("updated_address.html",ID=ID)




@app.route("/update_email")
def update_email():
    return flask.render_template('update_email.html')

@app.route("/updated_email",methods=["POST"])
def updated_email():
    email=flask.request.form["email"]
    ID=flask.request.form["memberID"]
    db=get_db()
    db.execute("UPDATE member SET email=(?) WHERE memberID=(?)",(email,int(ID)))
    db.commit()
    db.close()
    return flask.render_template("updated_email.html",ID=ID)
    
    

















if __name__== '__main__':
    app.run(port =1230, debug=True)

app.run(debug=True)
