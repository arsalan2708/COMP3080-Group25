


def createRatings(conn,c):
    print("creating ratings")
    c.execute('''CREATE TABLE ratings(
        tconst text not null,
        rating REAL not null,
        votes integer not null,
        FOREIGN KEY (tconst) REFERENCES titles(tconst) ON DELETE CASCADE ON UPDATE CASCADE
        );''')
    conn.commit()

def populateRating(conn,c,path):
    print("rating...titles")
    with open(path+"ratings.tsv") as f:
        f.readline()
        for data in f:
            d = data.strip('\r\n').split('\t')
            d[1]= float(d[1])
            d[2]= int(d[2])
            # print(d)
            c.execute('''INSERT INTO ratings VALUES(?,?,?)''',d)
        conn.commit()

def build(conn,path):
    cursor = conn.cursor()
    createRatings(conn,cursor)
    populateRating(conn,cursor,path)
    cursor.close()
