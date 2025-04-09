from flask import Flask, render_template, request, redirect, url_for, flash
import requests  
from database.models import db, Comment, Like, User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
import os
app.secret_key = os.urandom(24)  # generates a random 24-byte key



app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://web_news_sb7l_user:Z8aUR85bxJegovvOVRS9RNeVoKdnE2sv@dpg-cvr8dlvgi27c738ntveg-a.oregon-postgres.render.com/web_news_sb7l"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # ✅ Correct usage of the imported db

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def Load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
     
    
     db.create_all()

API_KEY = "f0437aadecd84637b2b306e1864af11e"



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return "Invlid credenitials"
    return render_template('login.html')

    

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username = request.form['username']

        password=request.form['password']
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('signup'))
        user=User(username=username)
        user.set_password(password) 

        db.session.add(user)
        db.session.commit()
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')




def load_news(query="keyword"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get('articles', [])

@app.route('/home')
def home():
    categories = ['Sports', 'Business', 'Technology', 'Entertainment']
    return render_template('home.html', categories=categories)

@app.route('/category/<cat>')
def category(cat):
    articles = load_news(cat)
    return render_template('index.html', data=articles, category=cat)

@app.route('/news/<int:news_id>')
def more_info(news_id):
    news = load_news()
    news_item = news[news_id] if 0 <= news_id < len(news) else None

    like = Like.query.filter_by(news_id=news_id).first()
    like_count = like.count if like else 0

    comments = Comment.query.filter_by(news_id=news_id).all()

    return render_template('news_detail.html',
                           news_item=news_item,
                           news_id=news_id,
                           likes=like_count,
                           comments=comments)



@app.route('/like/<int:news_id>', methods=['POST'])
@login_required
def like(news_id):
    like = Like.query.filter_by(news_id=news_id).first()
    if like:
        like.count += 1
    else:
        like = Like(news_id=news_id, count=1)
        db.session.add(like)
    db.session.commit()
    return redirect(url_for('more_info', news_id=news_id))



@app.route('/comment/<int:news_id>', methods=['POST'])
@login_required
def comment(news_id):
    user_comment = request.form.get('comment')
    if user_comment:
        new_comment = Comment(news_id=news_id, content=user_comment,user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('more_info', news_id=news_id))

if __name__ == '__main__':
    app.run(debug=True)
