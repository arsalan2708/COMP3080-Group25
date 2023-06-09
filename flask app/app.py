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
    q = f" select * from {varb}"
    return outQuery(q)

@app.route('/get/<varb>', methods=['POST'])
def get(varb):
    q = f" select {varb}"
    return outQuery(q)

@app.route('/getType/<req>/<byVal>/<typ>/<value>', methods=['POST'])
def getRating(req,byVal,typ,value):
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
    
    return outQuery(q)


@app.route('/getTypeBetween/<req>/<byVal>/<value1>/<value2>', methods=['POST'])
def getTypeBetween(req,byVal,value1,value2):
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

    return outQuery(q)


@app.route('/actorsFor/<typ>/<tconst>', methods=['POST'])
def getactorsFor(typ,tconst):
    typFix = typ if typ!='movie' else 'movies'
    q = f''' select P.nconst, P.name as cast
            from ((people P JOIN actors A ON P.nconst = A.nconst) join {typFix} M ON M.tconst = A.tconst) 
            where A.tconst = '{tconst}'; '''

    return outQuery(q);

@app.route('/crewFor/<typ>/<tconst>', methods=['POST'])
def getcrewFor(typ,tconst):
    typFix = typ if typ!='movie' else 'movies'
    q = f''' select P.nconst, P.name as crew
            from ((people P JOIN crew A ON P.nconst = A.nconst) join {typFix} M ON M.tconst = A.tconst) 
            where A.tconst = '{tconst}' '''

    return outQuery(q);


@app.route('/listEp/<tconst>', methods=['POST'])
def getEpList(tconst):
    q = f''' select E.tconst, (case when T.title is null then 'Un-Released' else T.title end) as title
            , season, epNo as episodeNumber, (case when runTime is null then 'unKnown' else runTime end) as runTime,
             (case when R.rating is null then 'N/A' else R.rating end) as rating
            from episodes E full outer join titles T ON E.tconst = t.tconst
            full outer join ratings R on E.tconst = R.tconst
            where parent_tconst = '{tconst}'
            order by season, epNo; '''
    return outQuery(q);


@app.route('/knownFor/<nconst>', methods=['POST'])
def getKnownFor(nconst):
    q = f'''select T.tconst as tconst, fType, title, T.startYear as releasedYear
            from people P JOIN crew A ON P.nconst = A.nconst
    join titles T on T.tconst = A.tconst
    where A.nconst = '{nconst}' and T.fType in ('movie','tvSeries') 
    UNION
    select T.tconst, fType, title , T.startYear as realeasedYear
    from people P JOIN actors A ON P.nconst = A.nconst
    join titles T on T.tconst = A.tconst
    where A.nconst = '{nconst}' and T.fType in ('movie','tvSeries') '''
    return outQuery(q);


@app.route('/getRating/<format>/<tconst>', methods=['POST'])
def getCalcRating(format,tconst):
    q1= f'''select rating from(
select E.parent_tconst as tconst, round(avg(rating),2) as rating 
        from episodes E 
        join ratings R ON R.tconst=E.tconst 
        group by E.parent_tconst
        order by parent_tconst desc ) where tconst = '{tconst}' '''

    q2 = f'''select  (case
    when count(rating) = 0 
    then 'un-rated'
    else rating
    end) as rating from ratings where tconst = '{tconst}' '''

    q = q1 if format=='tvSeries' else q2
    
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()
    res= cursor.execute(q)
    result = list()
    for r in res.fetchall():
        result.append(r[0]);

    cursor.close()
    conn.close()
    return result

@app.route('/getTimeStamp/<tconst>', methods=['POST'])
def getTimeStamp(tconst):
    q= f''' 
    with timeStamp as (
select T.tconst,T.title, T.fType, T.startYear , tv.endYear from titles T
full outer join tvSeries tv on tv.tconst = T.tconst
where fType in ('movie','tvSeries')
)

select title, fType, ( case when fType ='tvSeries'
        then   (case
    when endYear=0
    then startYear || ' - Present'
    else startYear || ' - ' || endYear end)
    else startYear
end) as timeFrame from timeStamp where tconst = '{tconst}'
    '''
    
    return outQuerysimple(q)


@app.route('/getPersonInfo/<nconst>', methods=['POST'])
def getPInfo(nconst):
    q= f''' select * from people where nconst = '{nconst}' '''
    return outQuerysimple(q)
    


@app.route('/workedWith/<nconst>', methods=["POST"])
def workedWith(nconst):
    q= f''' with alljobs as (select tconst, nconst from actors
            UNION
            select tconst, nconst from crew)

select distinct Z.nconst, name
from alljobs join people Z on alljobs.nconst = Z.nconst
where Z.nconst != '{nconst}' and alljobs.tconst IN (
    select A.tconst
    from (((people P JOIN alljobs A ON P.nconst = A.nconst) ) 
    join titles T on T.tconst = A.tconst)
    where A.nconst = '{nconst}' )
order by name asc; '''
    return outQuery(q)

@app.route('/getAttri/<const>', methods=["POST"])
def idInfo(const):
    q1 = f''' select genre from genres where tconst= '{const}' '''
    q2 = f''' select profession from profession where nconst= '{const}' '''
    
    q = q2 if ('nm' in const) else q1 

    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()
    res= cursor.execute(q)
    result = list()
    for r in res.fetchall():
        result.append(r[0]);

    cursor.close()
    conn.close()
    return result

@app.route('/getByAttri/<typ>/<reqVal>', methods=["POST"])
def byAttri (typ,reqVal):
    q1= f''' select * from titles where fType in ('movie','tvSeries') and tconst in (select tconst from genres where genre='{reqVal}')  order by startYear ''';
    q2= f''' select * from people where nconst in (select distinct nconst from profession where profession = '{reqVal}')  ''';

    q = q2 if ('people' in typ) else q1 
    print(q)
    return outQuery(q)

   
def outQuerysimple(q):
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()
    res= cursor.execute(q)
    result = list()
    for r in res.fetchall():
        result.append(r);

    cursor.close()
    conn.close()
    return result


def outQuery(q):
    conn = sqlite3.connect(dbPath,uri=True)
    cursor = conn.cursor()
    result =  ['No result found']

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



webbrowser.open('http://127.0.0.1:2708/')
app.run(debug=True,port=2708, host='0.0.0.0')

print("\nprogram execution complete!")