from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Function to load posts from a text file
def load_posts():
    try:
        with open('posts.txt', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save posts to a text file
def save_posts(posts):
    with open('posts.txt', 'w') as file:
        json.dump(posts, file)

# Ensure that the file exists before running the app
if not os.path.exists('posts.txt'):
    with open('posts.txt', 'w') as file:
        file.write('[]')

posts = load_posts()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        post = {'text': text, 'likes': 0, 'comments': []}
        posts.append(post)
        save_posts(posts)  # Save posts to the text file
        return redirect(url_for('index'))
    return render_template('index.html', posts=posts)

@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    if 0 <= post_id < len(posts):
        posts[post_id]['likes'] += 1
        save_posts(posts)  # Save posts to the text file
    return redirect(url_for('index'))

@app.route('/comment_post/<int:post_id>', methods=['POST'])
def comment_post(post_id):
    if 0 <= post_id < len(posts):
        comment = request.form['comment']
        posts[post_id]['comments'].append(comment)
        save_posts(posts)  # Save posts to the text file
    return redirect(url_for('index'))

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 0 <= post_id < len(posts):
        del posts[post_id]
        save_posts(posts)  # Save posts to the text file
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def view_post(post_id):
    if 0 <= post_id < len(posts):
        post = posts[post_id]
        return render_template('post.html', post=post)
    return redirect(url_for('index'))

@app.route('/comment/<int:post_id>')
def view_comment(post_id):
    if 0 <= post_id < len(posts):
        post = posts[post_id]
        return render_template('comment.html', post=post)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)