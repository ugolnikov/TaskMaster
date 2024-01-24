from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class UserForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email')
    submit = SubmitField('Add User')

@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    form = UserForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index.html', users=users, form=form)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
