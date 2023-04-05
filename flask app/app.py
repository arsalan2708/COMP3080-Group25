from flask import Flask, render_template, request
import sqlite3
import os



dbPath = 'file:../database/database.db?mode=ro'

app = Flask(__name__)

@app.route('/')
def show_home():
    return render_template("index.html")

@app.route('/getAllGenre', methods=["POST"])
def getAllGenre():
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()
    cursor.execute('select distinct genre from genres order by genre asc')
    
    genres = list()

    for g in cursor.fetchall():
        genres.append(g[0])
    
    conn.close()
    return genres


@app.route('/getProfessions', methods=["POST"])
def getProfessions():
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()
    cursor.execute('select distinct profession from profession order by profession asc')
    
    proff = list()

    for g in cursor.fetchall():
        proff.append(g[0])
    
    conn.close()
    return proff




@app.route('/getAll/<varb>', methods=['POST'])
def test(varb):
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()

    try:
        result = list()
        res = cursor.execute(f" select * from {varb}")
        names = [description[0] for description in cursor.description]

        first = res.fetchone();
        if first is not None:
            result.append(names)
            result.append(first)
            for r in res.fetchall():
                result.append(r)
        else:
            result =  ['No result found']

    except:
        result =  ['No result found'] , 400
    
    return result


def readInput(input):
    data = input.split('+')
    for i in range(len(data)):
        data[i] = tuple(data[i].split('='))
    return data


if '__name__' == '__main__' :
    app.run(debug=False,port=2780, host='0.0.0.0')

print("\nprogram execution complete!")