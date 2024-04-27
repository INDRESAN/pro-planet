from flask import render_template,request,Flask,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from sqlalchemy import desc

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
    email = db.Column(db.String(20),nullable=True)
    points = db.Column(db.Integer,default=50)
    upvotes = db.Column(db.Integer,default=0)
    Badge = db.Column(db.String(20),default="Rookie")

class Task(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    Description = db.Column(db.String(240),nullable=False)

class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    Description = db.Column(db.String(240),nullable=False)
    img_url= db.Column(db.String(120), nullable=False)

class Post_Participant(db.Model):
    qid= db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, nullable=True)
    tid = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(120), nullable=False)
    Participating = db.Column(db.Boolean,default=False)
    Posted = db.Column(db.Boolean,default=False)


with app.app_context():
    db.create_all()


app.secret_key="superhighsecretlock"

@app.route('/',methods=['POST','GET'])
def index():
    return render_template("index.html")


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        uname = request.form["uname"]
        email = request.form["email"]
        pwd = request.form["pswd"]
        user = User(password=pwd, fullname=uname,email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login',methods=['POST','GET'])
def login():
    msg=''
    if request.method=='POST':
        uname = request.form["uname"]
        pwd = request.form["pswd"]
        auth = User.query.filter_by(fullname=uname,password=pwd).all()
        if auth:
            session['uname']=uname
            session['pwd']=pwd
            return redirect(url_for('home'))
        else:
            msg="Invalid Username/Password"
    return render_template("login.html",message=msg)


@app.route('/home',methods=['POST','GET'])
def home():
    posts = Post.query.all()
    profile = User.query.filter_by(fullname=session['uname'],password=session['pwd']).all()
    if request.method=='POST':
        uname=request.form['say']
        add_points = User.query.filter_by(fullname=uname).first()
        add_points.points+=50
        db.session.commit()

    return render_template("home.html",profile=profile,posts=posts)

@app.route('/profile',methods=['POST','GET'])
def profile():
    profile = User.query.filter_by(fullname=session['uname'],password=session['pwd']).all()
    return render_template("Profile.html",profile=profile)


@app.route('/task',methods=['POST','GET'])
def task():
    if Post_Participant.query.filter_by(user=session['uname']).all():
        tasks=Task.query.filter(~Post_Participant.query.filter_by(tid=Task.tid, user=session['uname'], Participating=True).exists()
).all()
    else:
        tasks=Task.query.all()
    if request.method=='POST':
        id=request.form['say']
        add_participation = Post_Participant(tid=id,user=session['uname'],Participating = True)
        db.session.add(add_participation)
        db.session.commit()
        return redirect(url_for("task"))
    return render_template("task_accept.html",tasks=tasks)

@app.route('/add_task',methods=['POST','GET'])
def addTask():
    msg=''
    if request.method=='POST':
        title = request.form["title"]
        desc = request.form["desc"]
        task = Task(title=title,Description=desc)
        db.session.add(task)
        db.session.commit()
    return render_template("add_task.html",message=msg)

@app.route('/post',methods=['POST','GET'])
def post():
    if request.method=='POST':
        title = request.form["title"]
        desc = request.form["desc"]
        file = request.files['image']
        if file.filename == '':
            return "No selected file"
        if file:
        # Specify the path where you want to save the uploaded image
            file.save('static/' + file.filename)
        post = Post(title=title,Description=desc,owner=session['uname'],img_url=file.filename)
        db.session.add(post)
        db.session.commit()
    return render_template("post.html")

@app.route('/leaderboard',methods=['POST','GET'])
def leaderboard():
        leaderboard = User.query.order_by(User.points.desc()).all()
        leaderboard = [[leaderboard.index(i)+1,i] for i in leaderboard]
        return render_template("leaderboard.html",leaderboard=leaderboard)
 
if __name__ == '__main__':
    app.run(debug=True,port=5001)