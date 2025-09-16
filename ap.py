from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # change this to a strong secret in production

# Mail configuration (values should be set in Render dashboard → Environment)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")   # set in Render
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")   # set in Render

mail = Mail(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("⚠ All fields are required!", "danger")
        return redirect(url_for("home"))

    # Save to local file (optional, for record keeping)
    with open("messages.txt", "a") as f:
        f.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n{'-'*40}\n")

    try:
        msg = Message(
            subject="New Internship Finder Message",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f"From: {name} <{email}>\n\n{message}"
        )
        mail.send(msg)
        flash("✅ Message sent successfully!", "success")
    except Exception as e:
        flash(f"⚠ Saved but email not sent: {str(e)}", "warning")

    return redirect(url_for("home"))

if __name__ == "__main__":
    # host=0.0.0.0 allows Render to expose the app
    app.run(host="0.0.0.0", port=5000)
