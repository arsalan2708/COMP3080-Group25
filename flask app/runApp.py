from flask import Flask, render_template, request
import sqlite3

dbPath = '../database/database.db'

app = Flask(__name__)

@app.route('/')
def show_home():
    return render_template("index.html")

@app.route('/getAllGenre', methods=["POST"])
def searchBy():
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute('select distinct genre from genres')
    
    genres = list()
    for g in cursor.fetchall():
        genres.append(g[0])
    
    conn.close()
    return genres


@app.route('/getReq/<varb>', methods=['POST'])
def test(varb):
    print(f"test succ : got {varb}")
    return readInput(varb)


def readInput(input):
    data = input.split('+')
    for i in range(len(data)):
        data[i] = tuple(data[i].split('='))
    return data





app.run(debug=True,port=2780)
print("\nprogram execution complete!")