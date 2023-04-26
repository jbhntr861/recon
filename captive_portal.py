from flask import Flask, redirect, request, session, url_for
import os
from OpenSSL import SSL

class CaptivePortal:
    def __init__(self, certificate_path, private_key_path, secret_key):
        self.app = Flask(__name__)
        self.app.secret_key = secret_key

        self.context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(os.path.abspath(certificate_path), os.path.abspath(private_key_path))

        self.app.route('/')(self.index)
        self.app.route('/login', methods=['GET', 'POST'])(self.login)
        self.app.route('/logout')(self.logout)

    def run(self):
        self.app.run(ssl_context=self.context)

    def index(self):
        if 'username' in session:
            return f'Hello, {session["username"]}!<br><a href="/logout">Log out</a>'
        else:
            return redirect(url_for('login'))

    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # Validate username and password here (e.g. check against a database)
            if username == 'admin' and password == 'password':
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return 'Invalid username or password'
        else:
            return '''
                <form method="post">
                    <label>Username:</label>
                    <input type="text" name="username"><br>
                    <label>Password:</label>
                    <input type="password" name="password"><br>
                    <input type="submit" value="Log in">
                </form>
            '''

    def logout(self):
        session.pop('username', None)
        return redirect(url_for('index'))
