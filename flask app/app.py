from flask import Flask, render_template, request
import sqlite3
import webbrowser



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

@app.route('/get/<varb>', methods=['POST'])
def get(varb):
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()

    try:
        result = list()
        res = cursor.execute(f" select {varb}")
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
        result =  ['No result found'] , 404
    
    cursor.close()
    conn.close()
    return result

@app.route('/getType/<req>/<byVal>/<typ>/<value>', methods=['POST'])
def getRating(req,byVal,typ,value):
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()

    print(byVal)
    q1 = f'''select t.* , m.runTime, r.rating from titles t 
        join movies m on t.tconst = m.tconst  join ratings r on t.tconst = r.tconst where {byVal} {typ} {value} order by {byVal}'''

    q2 = f'''select titles.*, tv.endYear, round(rating, 2) as rating
                        from(titles join  tvSeries tv on tv.tconst = titles.tconst join 
                                (select E.parent_tconst, avg(rating) as rating
                                from episodes E join ratings R ON R.tconst=E.tconst 
                                group by E.parent_tconst
                                order by parent_tconst desc) ON parent_tconst = titles.tconst) where {byVal} {typ} {value} order by {byVal}  '''

    q3 = f'''select * from titles where fType in ('movie','tvSeries') and {byVal} {typ} {value } order by {byVal} '''

    q = q3 if req=='titles' else (q1 if req=='movie' else q2) 

    try:
        result = list()
        res = cursor.execute(q)
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
    
    cursor.close()
    conn.close()
    return result


@app.route('/getTypeBetween/<req>/<byVal>/<value1>/<value2>', methods=['POST'])
def getTypeBetween(req,byVal,value1,value2):
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()

    q1 = f'''select t.* , m.runTime, r.rating from titles t 
        join movies m on t.tconst = m.tconst  join ratings r on t.tconst = r.tconst where {byVal}>={value1} and {byVal}<={value2} order by {byVal}'''

    q2 = f'''select titles.*, tv.endYear, round(rating, 2) as rating
                        from(titles join  tvSeries tv on tv.tconst = titles.tconst join 
                                (select E.parent_tconst, avg(rating) as rating
                                from episodes E join ratings R ON R.tconst=E.tconst 
                                group by E.parent_tconst
                                order by parent_tconst desc) ON parent_tconst = titles.tconst) where {byVal}>={value1} and {byVal}<={value2} order by {byVal}  '''

    q3 = f'''select * from titles where fType in ('movie','tvSeries') and {byVal}>={value1} and {byVal}<={value2} order by {byVal} '''

    q = q3 if req=='titles' else (q1 if req=='movie' else q2) 

    try:
        result = list()
        res = cursor.execute(q)
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
    
    cursor.close()
    conn.close()
    return result




def readInput(input):
    data = input.split('+')
    for i in range(len(data)):
        data[i] = tuple(data[i].split('='))
    return data


if __name__ == '__main__' :
    webbrowser.open('http://127.0.0.1:2708/')
    app.run(debug=True,port=2708, host='0.0.0.0')

print("\nprogram execution complete!")