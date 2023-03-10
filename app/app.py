import sqlite3
from flask import * 
from kernel4 import IDSearcher
import time
import flask
import flask_login

app = Flask(__name__)
id_searcher = IDSearcher()
app.secret_key = 'xU.Wy;*5DA8YL:[}'  # Change this!
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {
    
    }

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <center>
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='token' id='token' placeholder='token'/>
                <input type='submit' name='submit'/>
               </form>
               </center>
               '''

    email = flask.request.form['email']
    if email in users and flask.request.form['token'] == users[email]['token']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('search_page'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


@app.route('/')
@flask_login.login_required
def search_page():
    # return flask.redirect(flask.url_for('login'))
    return render_template('search.html')

@app.route('/search', methods=['POST'])
@flask_login.login_required
def search_ids():
    flag = False
    search_type = int(request.form['search_type'])
    f1 = request.form['f1']
    f2 = request.form['f2']
    if not f2:
        f2 = int(f1) + 1
        num_ids = 1
    else:
        num_ids = int(f2) - int(f1)
    etime_max = 2
    if num_ids <= 10000:
        try:
            start_time = time.time()
            found_ids = id_searcher.search_ids(search_type, f1, f2)
            flag = True
            real_time = round(time.time() - start_time, 2)
            return render_template('search.html', real_time=real_time, found_ids=found_ids, etime_max=etime_max, flag=flag)
        except:
            return render_template('search.html', error='An error occurred while processing your request', flag=flag)
    else:
        return render_template('search.html', error='The number of IDs must be less than 10000', flag=flag)

# cp db then show 2nd db here as backup
@app.route('/database')
def show_database():
    try:
        conn = sqlite3.connect('../db/mooshyab7.db')
        c = conn.cursor()
        c.execute("SELECT * FROM data")
        data = c.fetchall()
        conn.close()
        return render_template('database.html', data=data)
    except:
        return render_template('database.html', error='An error occurred while connecting to the database')

if __name__ == '__main__':
    app.run(debug=True)
