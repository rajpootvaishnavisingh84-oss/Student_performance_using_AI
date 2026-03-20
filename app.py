from flask import Flask, render_template, request, redirect, url_for, session
import random
from werkzeug.security import generate_password_hash, check_password_hash

# ML prediction file
from predict import predict_grade

app = Flask(__name__)
app.secret_key = "secret123"

# simple user storage
users = {}


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------
@app.route("/login")
def login():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    session["captcha"] = num1 + num2

    return render_template("login.html", num1=num1, num2=num2)


# ---------------- REGISTER ----------------
@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/do_register", methods=["POST"])
def do_register():

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"] 
    if len(password) < 6:
     return render_template("register.html", error="Password must be at least 6 characters ")  


    if email in users:
        return render_template("register.html", error="User already exists")

    users[email] = generate_password_hash(password)

    return redirect(url_for("login"))


# ---------------- LOGIN CHECK ----------------
@app.route("/do_login", methods=["POST"])
def do_login():

    email = request.form["email"]
    password = request.form["password"]
    captcha = request.form["captcha"]

    if email not in users:
        return render_template("login.html", error="User not registered", num1=0, num2=0)

    if not check_password_hash(users[email], password):
        return render_template("login.html", error="Incorrect password", num1=0, num2=0)

    if int(captcha) != session.get("captcha"):
        return render_template("login.html", error="Captcha incorrect", num1=0, num2=0)

    session["user"] = email

    return redirect(url_for("dashboard"))


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# ---------------- ML PREDICTION ----------------
@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect(url_for("login"))

    try:
        study_hours = float(request.form["study_hours"])
        attendance = float(request.form["attendance"])
        participation = float(request.form["participation"])
    except:
        return "Invalid input"

    # validation
    if not (0 <= attendance <= 100):
        return "Attendance must be between 0 and 100"

    # ML prediction
    features = [study_hours, attendance, participation]
    prediction = predict_grade(features)

    # 🔥 your real accuracy
    accuracy = 0.67

    return render_template(
        "dashboard.html",
        prediction=prediction,
        accuracy=accuracy,
        study_hours=study_hours,
        attendance=attendance,
        participation=participation
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)