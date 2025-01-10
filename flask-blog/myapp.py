#import
from flask import Flask , render_template,request,redirect,flash,jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin,LoginManager,login_user,login_required,logout_user,current_user
from datetime import datetime
from werkzeug.security import generate_password_hash , check_password_hash
import os
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from flask_wtf import CSRFProtect
import pytz
from forms import LoginForm, SignupForm
from urllib.parse import urlparse, urljoin
from sqlalchemy.orm import relationship
from forms import DeleteForm,EditForm,CreateForm  
from flask import render_template, redirect, url_for, flash, request
from forms import LoginForm, SignupForm
from sqlalchemy import text


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (
        test_url.scheme in ('http', 'https') and
        ref_url.netloc == test_url.netloc
    )


app = Flask(__name__)
csrf = CSRFProtect(app)

# Flaskとデータベースの接続設定
db = SQLAlchemy()
DB_INFO = {
    'user': 'postgres',
    'password': '0000',
    'host': 'localhost',
    'name': 'postgres',
    'port': '1234'
}


if app.debug:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://{user}:{password}@{host}:{port}/{name}'.format(**DB_INFO)
else:
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url.replace("postgres://", "postgresql+psycopg://")
    else:
        # 環境変数が設定されていない場合のフォールバック
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://{user}:{password}@{host}:{port}/{name}'.format(**DB_INFO)


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
migrate = Migrate(app, db)


#テーブルの定義
class Post(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100) , nullable = False)
    body = db.Column(db.String(1000) , nullable = False)
    tokyo_timezone = pytz.timezone('Asia/Tokyo')
    created_at = db.Column(db.DateTime , nullable = False , default= datetime.now(tokyo_timezone))
    img_name = db.Column(db.String(1000) , nullable =True)
    likes = db.Column(db.Integer, nullable=False, server_default=text('0'))  # いいね数の追加
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,server_default=text('1'))
    

    # アイコンカウントフィールドの追加（server_defaultを設定）
    icon1_count = db.Column(db.Integer, nullable=False, server_default='0')
    icon2_count = db.Column(db.Integer, nullable=False, server_default='0')
    icon3_count = db.Column(db.Integer, nullable=False, server_default='0')
    
    user=relationship('User' , backref ='posts')
    
#create Like table (12.20)
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)  # ON DELETE CASCADE を追加
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)



    





#flaskのセッション情報の暗号化に使用
if app.debug: #ローカルで動かすとき用
    app.config["SECRET_KEY"] = os.urandom(24)
else:  #heroku上で動くとき用
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')


#login管理用
login_manager = LoginManager()
login_manager.init_app(app)


#ユーザー管理データベースの定義
class User(UserMixin , db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(1000) , unique = True , nullable = False)
    password = db.Column(db.String(1000)  , nullable = False)


#現在のユーザを識別するためのコード
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#引数には文字列がくるため整数型に変換する


#index関数
@app.route("/")
def index():
    # 全ての投稿を取得し、作成日時の降順でソート
    posts = Post.query.order_by(Post.created_at.desc()).all()
    posts = [
        {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'img_name': post.img_name,
            'created_at': post.created_at.date(),
            'likes': post.likes,
            'icon1_count' : post.icon1_count,
            'icon2_count' : post.icon2_count,
            'icon3_count' : post.icon3_count,
            'username' : post.user.username # 投稿者のユーザー名を追加(12.20)
        }
        for post in posts
    ]
    # いいね数でソートし、上位3つの投稿を取得
    top_posts = Post.query.order_by(Post.likes.desc()).limit(10).all()
    top_posts = [
        {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'img_name': post.img_name,
            'created_at': post.created_at.date(),
            'likes': post.likes,
            'icon1_count' : post.icon1_count,
            'icon2_count' : post.icon2_count,
            'icon3_count' : post.icon3_count,
            'username' : post.user.username # 投稿者のユーザー名を追加(12.20)
        }
        for post in top_posts
    ]
    return render_template("index.html", posts=posts, top_posts=top_posts)


#explanation関数
@app.route('/explanation')
def explanation():
    return render_template('explanation.html')


#explanationvideo関数
@app.route('/explanationvideo')
def explanationvideo():
    return render_template('explanationvideo.html')


@app.route('/ranking')
def ranking():
    # いいね数で降順にソートされた投稿を取得
    posts = Post.query.order_by(Post.likes.desc()).all()
    # 投稿データを準備
    posts = [
        {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'img_name': post.img_name,
            'created_at': post.created_at.date(),
            'likes': post.likes,
            'icon1_count': post.icon1_count,
            'icon2_count': post.icon2_count,
            'icon3_count': post.icon3_count,
            'username' : post.user.username # 投稿者のユーザー名を追加(12.20)
        }
        for post in posts
    ]
    return render_template('ranking.html', posts=posts)



#readmore関数
@app.route("/<int:post_id>/readmore")
def readmore(post_id):
    post = Post.query.get(post_id)
    post = {
        'id': post.id,
        'title': post.title,
        'body': post.body,
        'img_name': post.img_name,
        'created_at': post.created_at.date(),
        'icon1_count': post.icon1_count,
        'icon2_count': post.icon2_count,
        'icon3_count': post.icon3_count
    }
    return render_template('readmore.html', post=post)



#admin関数
@app.route("/admin")
@login_required
def admin():
    # desk()は降順 なしだと昇順
    user_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).all()
    posts = [
        {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'img_name': post.img_name,
            'created_at': post.created_at.date(),
        }
        for post in user_posts
    ]
    delete_forms = {post['id']: DeleteForm() for post in posts}
    return render_template("admin.html", posts=posts, delete_forms=delete_forms)




#create関数
import logging
# ログの設定
logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        file = form.img.data

        # アイコンカウントの取得
        try:
            icon1_count = int(form.icon1_count.data)
            icon2_count = int(form.icon2_count.data)
            icon3_count = int(form.icon3_count.data)
            app.logger.debug(f"Icon counts - Icon1: {icon1_count}, Icon2: {icon2_count}, Icon3: {icon3_count}")
        except (ValueError, TypeError):
            flash('アイコンの選択数が無効です。', 'danger')
            app.logger.debug("Invalid icon counts received.")
            return redirect(request.url)
        
        total_icons = icon1_count + icon2_count + icon3_count
        app.logger.debug(f"Total icons selected: {total_icons}")

        if total_icons != 6:
            flash('アイコンの選択は合計6回必要です。', 'danger')
            app.logger.debug("Total icons not equal to 6.")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            created_at = datetime.now(pytz.timezone('Asia/Tokyo'))
            img_path = os.path.join(app.static_folder, 'img', filename)
            file.save(img_path)
            app.logger.debug(f"Image saved at {img_path}")

            post = Post(
                title=title,
                body=body,
                img_name=filename,
                created_at=created_at,
                user_id=current_user.id,
                icon1_count=icon1_count,
                icon2_count=icon2_count,
                icon3_count=icon3_count
            )
            db.session.add(post)
            db.session.commit()
            flash('投稿が作成されました', 'success')
            app.logger.debug("Post created successfully.")
            return redirect(url_for('index'))
        else:
            flash('有効な画像ファイルをアップロードしてください', 'danger')
            app.logger.debug("Invalid image file uploaded.")
            return redirect(request.url)
    
    if form.errors:
        app.logger.debug(f"Form errors: {form.errors}")

    return render_template('create.html', form=form)


#signup関数
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data


        # ユーザー名の重複確認
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('ユーザ名は既に存在します。')
            return redirect(url_for('signup'))


        # パスワードのハッシュ化
        hashed_pass = generate_password_hash(password)
        user = User(username=username, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash('アカウント登録が完了しました。ログインしてください。')
        return redirect(url_for('login'))


    return render_template('signup.html', form=form)


#login関数
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        next_page = request.args.get('next')


        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('ユーザー名/パスワードが違います')
            return redirect('/login')


    next_page = request.args.get('next')
    return render_template('login.html', form=form, next=next_page)


#logout関数
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



#update関数の更新(10/30)
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('他のユーザーの投稿を編集することはできません。')
        return redirect(url_for('index'))
    
    form = EditForm(obj=post)  # 既存の投稿データをフォームにロード

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data

        # アイコンカウントの取得
        try:
            icon1_count = int(form.icon1_count.data)
            icon2_count = int(form.icon2_count.data)
            icon3_count = int(form.icon3_count.data)
            total_icons = icon1_count + icon2_count + icon3_count
            if total_icons != 6:
                flash('アイコンの選択は合計6回必要です。')
                return redirect(request.url)
        except (ValueError, TypeError):
            flash('アイコンの選択数が無効です。')
            return redirect(request.url)
        
        post.icon1_count = icon1_count
        post.icon2_count = icon2_count
        post.icon3_count = icon3_count

        # 画像の更新
        file = form.img.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.static_folder, 'img', filename)
            file.save(img_path)
            post.img_name = filename
        elif file and not allowed_file(file.filename):
            flash('有効な画像ファイルをアップロードしてください。')
            return redirect(request.url)

        db.session.commit()
        flash('投稿が更新されました。')
        return redirect(url_for('admin'))
    else:
        # フォームが初期表示またはエラーがある場合
        return render_template('update.html', post=post, form=form)




#delete関数
@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    # admin ビューで生成した DeleteForm を取得
    delete_form = DeleteForm()
    if delete_form.validate_on_submit():
        post = Post.query.get_or_404(post_id)
        if post.user_id != current_user.id:
            flash('他のユーザーの投稿を削除することはできません。')
            return redirect(url_for('index'))


        db.session.delete(post)
        db.session.commit()
        flash('投稿が削除されました。')
    else:       
        flash('不正なリクエストです ')
    return redirect(url_for('admin'))



@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)


#modify likes function(12.20)
@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # すでにいいねされているか確認
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing_like:
        return jsonify({'error': 'この投稿には既にいいねしています'}), 400
    
    # いいねを記録
    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.session.add(new_like)
    post.likes += 1
    db.session.commit()
    
    return jsonify({'likes': post.likes})
