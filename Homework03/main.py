from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash
from models import db, User
from forms import RegistrationForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = '123'
db.init_app(app)
csrf = CSRFProtect(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.route('/')
def index():
    return redirect(url_for('reg'))


@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        user = User(name, surname, email, password)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
