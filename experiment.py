from datetime import datetime
from flask import Flask,render_template,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm,PostForm
from flask_bcrypt import Bcrypt


app=Flask(__name__)
app.config['SECRET_KEY']='00a83c15f9c2fbb57ff47c439452b3a5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)




class User(db.Model):
    __tablename__='users'
    id= db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('post', backref='user',lazy='dynamic')
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Post(db.Model):
    __tablename__='posts'
    id= db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    description=db.Column(db.Text,nullable=False)
    duedate=db.Column(db.DateTime,nullable=False)
    priority = db.Column(db.Integer, nullable=False, default='0')
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f"post('{self.title}','{self.descripion}','{self.duedate}','{self.priority}')"




@app.route("/")
@app.route("/home")
def home(): 
    posts=db.session.query(Post).all()                
    return render_template('home.html',title='home',posts=posts)
                           
                           
@app.route("/about")
def about():
    return render_template('about.html',title='About')


@app.route("/todo")
def todo():
    return render_template('todo.html',title='Todo')

@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!, You aree now able to log in','Success')
        return redirect(url_for('todo'))
    return render_template('register.html',title='register',form=form)
    
@app.route("/login")
def login():
    form=LoginForm()
    return render_template('login.html',title='login',form=form)

@app.route("/post",methods=['GET','POST'])
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        flash('your post was created!','Success')
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html',title='new post',form=form)

@app.route("/post/<int:post_id>")    
def post(post_id):
    post=db.session.query(Post).get(post_id)
    return render_template('post.html', tile=post.title,post=post)

@app.route("/post/<int:post_id>/update")  
def update_post(post_id): 
    post=db.session.query(Post).get(post_id)
    form=PostForm()
    return render_template('create_post.html',title='update post',form=form)

@app.route("/post/<int:post_id>/delete")  
def delete_post(post_id):  
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))
    
    
    
    
    
if __name__=='__main__':
    app.run(debug=True, use_reloader=False)
