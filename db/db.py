from kernel3 import IDSearcher
import sqlite3
from multiprocessing import Pool


# # Create a connection to the database
# conn = sqlite3.connect('mooshyab7.db')

# # Create a cursor object to execute SQL statements
# c = conn.cursor()

# # Create the 'data' table
# c.execute('''
#           CREATE TABLE data (
#               Id INTEGER PRIMARY KEY,
#               Name TEXT,
#               MadrakId INTEGER,
#               IdNumber INTEGER,
#               Title TEXT,
#               Number TEXT,
#               Date TEXT
#           )
#           ''')

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

def main():
    anon1 = IDSearcher()
    l = anon1.search_ids(1, 928)
    print(l)
    # anon1.save_to_file(f)

if __name__ == "__main__":
    main()
# --------------------------------------------------------------

#--------------------------------------------------------------
# from flask import Flask, render_template, request, jsonify
# import sqlite3
# import requests

# app = Flask(__name__)

# @app.route("/")
# def home():
#     conn = sqlite3.connect('mooshyab7.db')
#     c = conn.cursor()
#     c.execute("SELECT * FROM data")
#     data = c.fetchall()
#     conn.close()
#     return render_template("home.html", data=data)


# if __name__ == "__main__":
#     app.run(debug=True)
