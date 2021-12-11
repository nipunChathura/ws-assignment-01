from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

import db_connection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    deposit_price = db.Column(db.Double(80), unique=True, nullable=False)
    guarantee_status = db.Column(db.Boolean(120), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Lon(db.Model):
    long_id = db.Column(db.Integer, primary_key=True)
    apply_user_id = db.Column(db.Integer(80), nullable=False)
    guarantee_user_id = db.Column(db.Integer(120), unique=True)
    lon_price = db.Column(db.Double(120), unique=True, nullable=False)


db.create_all()
admin = User(username='admin', email='admin@example.com')
help_user = db_connection.UserHelper


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users")
def load_user():
    users = help_user.get_all()
    context = {
        "name": "User List",
        "students": users
    }
    return render_template("index.html", **context)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        data = request.form
        st = (data.get("name"), data.get("deposit_price"))
        help_user.insert(st)
    return render_template("user/create.html")


@app.route("/lon", methods=["GET", "POST"])
def lon_apply():
    user = help_user.get_user_by_id()
    context = {
        "user": user.name
    }
    if request.method == "POST":
        data = request.form
        st = (data.get("name"), data.get("deposit_price"))
        response = help_user.insert(st)
        return render_template("lon/apply.html", response)
    return render_template("lon/apply.html", **context)


if __name__ == "__name__":
    app.run(debug=True)
