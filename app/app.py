import sqlite3
from flask import Flask, render_template, request
from kernel4 import IDSearcher
import time

app = Flask(__name__)
id_searcher = IDSearcher()

@app.route('/')
def search_page():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
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
