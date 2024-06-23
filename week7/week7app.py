from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from week7 import User, Post, init_db, add_user, add_post, get_all_posts, get_post_by_id, update_post, delete_post

app = Flask(__name__)

# Database initialization
engine = create_engine("sqlite:///mydb.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Ensure the database and tables are created
Base = init_db()

# Routes
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
