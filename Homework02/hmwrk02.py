from flask import Flask, request, redirect, url_for, make_response
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    name = request.cookies.get('name')
    email = request.cookies.get('email')
    if not name or not email:
        return redirect(url_for('login'))
    context = {
        'name': name
    }
    return render_template('hello.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        response = make_response('', 302)
        response.headers['Location'] = '/'
        response.set_cookie('name', name)
        response.set_cookie('email', email)
        return response
    return render_template('form.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response('', 302)
    response.headers['Location'] = '/login'
    response.delete_cookie('name')
    response.delete_cookie('email')
    return response


if __name__ == '__main__':
    app.run(debug=True)
