


def createRatings(c):
    print("creating ratings")
    c.execute('''CREATE TABLE ratings(
        tconst varchar(30) not null,
        rating int not null,
        votes int not null,
        FOREIGN KEY (tconst) REFERENCES titles(tconst) ON DELETE CASCADE ON UPDATE CASCADE
        );''')
    c.commit()

def populateRating(c,path):
    print("rating...titles")
    with open(path+"ratings.tsv") as f:
        f.readline()
        for data in f:
            d = data.strip('\r\n').split('\t')
            d[1]= float(d[1])
            d[2]= int(d[2])
            # print(d)
            c.execute('''INSERT INTO ratings VALUES(?,?,?)''',d)
        c.commit()

def build(conn,path):
    cursor = conn.cursor()
    createRatings(cursor)
    populateRating(cursor,path)
    cursor.close()
