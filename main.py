from flask import Flask, render_template
import requests

posts = requests.get(url="https://api.npoint.io/a9f67db60d74f9a52874").json()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    selected_post = None
    for post in posts:
        if post["id"] == index:
            selected_post = post
    return render_template("post.html", selected_post=selected_post)


if __name__ == "__main__":
    app.run(debug=True)