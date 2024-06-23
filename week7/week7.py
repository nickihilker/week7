from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import DateTime
from datetime import datetime
from flask import Flask, render_template


Base = declarative_base()

# user model
class User(Base):
    __tablename__ = "User"
    id = Column("id", Integer, primary_key=True)
    firstname = Column("firstname", String, nullable=False)
    lastname = Column("lastname", String, nullable=False)
    gender = Column("gender", CHAR, nullable=False)
    username = Column("username", String, unique=True, nullable=False)
    password_hash = Column("password_hash", String, nullable=False)

    def __init__(self, firstname, lastname, gender, username, password):
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return f"{self.firstname} {self.lastname} ({self.gender})"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def init_db():
    engine = create_engine("sqlite:///mydb.db", echo=True)
    Base.metadata.create_all(bind=engine)
    return engine

# add new user
def add_user(firstname, lastname, gender, username, password):
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    new_user = User(firstname, lastname, gender, username, password)
    session.add(new_user)
    session.commit()
    session.close()

    print(f"Added user: {new_user}")

# example 
if __name__ == "__main__":
    add_user("Mike", "Smith", "M", "mike123", "securepassword")


# post model
class Post(Base):
    __tablename__ = "Post"
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String, nullable=False)
    content = Column("content", String, nullable=False)
    pub_date = Column("pub_date", DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f"Post(title={self.title}, author_id={self.user_id})"
    
# Add new post
def add_post(title, content, user_id):
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    new_post = Post(title, content, user_id)
    session.add(new_post)
    session.commit()
    session.close()

    print(f"Added post: {new_post}")

def get_all_posts():
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    posts = session.query(Post).all()
    session.close()
    return posts

def get_post_by_id(post_id):
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    post = session.query(Post).filter(Post.id == post_id).first()
    session.close()
    return post

def update_post(post_id, title=None, content=None):
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None

    if title:
        post.title = title
    if content:
        post.content = content

    session.commit()
    session.close()
    print(f"Updated post: {post}")
    return post

def delete_post(post_id):
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None

    session.delete(post)
    session.commit()
    session.close()
    print(f"Deleted post: {post}")
    return post


from flask import Flask, render_template

app = Flask(__name__)

@app.route('/posts', methods=['GET'])
def list_posts():
    posts = get_all_posts()
    return render_template('posts.html', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    post = get_post_by_id(post_id)
    if not post:
        return "Post not found", 404
    return render_template('post_detail.html', post=post)

if __name__ == "__main__":
    app.run(debug=True)
