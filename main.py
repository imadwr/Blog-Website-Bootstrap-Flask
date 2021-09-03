from flask import Flask, render_template, request
import requests
import smtplib
import os

posts = requests.get(url="https://api.npoint.io/a9f67db60d74f9a52874").json()
EMAIL = os.getenv("email")
PASSWORD = os.getenv("password")
to_address = os.getenv("address")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        message_to_send = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nmessage: {message}"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=to_address,
                msg=f"Subject: New Message From Blog\n\n{message_to_send}"
            )
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    selected_post = None
    for post in posts:
        if post["id"] == index:
            selected_post = post
    return render_template("post.html", selected_post=selected_post)


if __name__ == "__main__":
    app.run(debug=True)
