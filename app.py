from flask import render_template,request,Flask,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy


app=Flask(__name__)
#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adithya14255:1Wg3FwivuZDU@ep-twilight-mode-70634399-pooler.ap-southeast-1.aws.neon.tech/neon?sslmode=require'

# class for database preperation

class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True

# run database

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()


app.secret_key="superhighsecretlock"

@app.route('/',methods=['POST','GET'])
def index():
    return render_template("index.html")

@app.route('/add_worker',methods=['POST','GET'])
def add_worker():
    msg=''
    if request.method=='POST':
        auth = User.query.filter_by(fullname=session['uname'],password=session['pwd']).all()
        if auth:
            return redirect(url_for('home'))
        else:
            msg="Invalid Username/Password"
    return render_template("add_worker.html",message=msg)

'''@app.route('/add_request',methods=['POST','GET'])
def add_request():
    if request.method=='POST':
        ename = request.form["ename"]
        tj = request.form["tj"]
        dist = request.form["dist"]
        locality = request.form["locality"]
        pincode = request.form["pincode"]
        contact = request.form["contact"]
        workreq = request.form["workreq"]
        wage = request.form["wage"]

        query = "insert into request(wage,ename,tj,dist,locality,pincode,contact,workreq) values(%s,%s,%s,%s,%s,%s,%s,%s) ;"
        con.execute(query,(wage,ename,tj,dist,locality,pincode,contact,workreq))
        con.connection.commit()
        con.close()

        return redirect(url_for('home'))
  
    return render_template("add_request.html")'''

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        uname = request.form["uname"]
        pwd = request.form["pswd"]
        user = User(password=pwd, fullname=uname)
        db.session.add(user)
        db.session.commit()
        session['uname']=uname
        session['pwd']=pwd
        return redirect(url_for('add_worker'))
    return render_template('signup.html')

'''
@app.route('/home',methods=['POST','GET'])
def home():
    con=conn.connection.cursor()
    con.execute("select * from request;")
    result=con.fetchall()
    return render_template("home.html",result=result)

@app.route('/request_accept',methods=['POST','GET'])
def request_accept():
    con=conn.connection.cursor()
    con.execute("select ename,tj,locality,pincode,contact,wage from request where ename=%s")
    result=con.fetchall()
    return render_template("request_accept.html",result=result)

@app.route('/completion',methods=['POST','GET'])
def completion():
        con=conn.connection.cursor()
        query='delete from request where ename=%s;'
        con.execute(query)
        con.connection.commit()
        con.close()
        return render_template("completion.html")

'''

if __name__ == '__main__':
    app.run(debug=True,port=5001)