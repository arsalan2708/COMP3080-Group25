'''create episode table and populate episodes for each tvSeries'''

def create_episodes(conn,c):
    print("creating episodes")
    c.execute('''CREATE Table episodes(
            tconst text not null primary key,
            parent_tconst text not null,
            season INTEGER not null,
            epNo INTEGER not null,
            runTime INTEGER,

            FOREIGN KEY (parent_tconst) REFERENCES tvSeries(tconst) ON DELETE CASCADE ON UPDATE CASCADE            
        );''')
    conn.commit()


def numConvert(d):
    return None if d is None else int(d)

def pop_episode(conn,c,path):
    print("populating episodes")
    with open(path+"episode.tsv") as f:
        f.readline() #ignore header
        
        for data in f:
            data = data.strip().split('\t')
            if len(data)<5: data.append(None) #if there are 4 items in the line runTime is missing
            data[2] =numConvert(data[2])
            data[3] =numConvert(data[3])
            data[4] =numConvert(data[4])
            c.execute('''INSERT INTO episodes VALUES(?,?,?,?,?);''',data)
        conn.commit()

def build(conn,path):
    cursor = conn.cursor()
    create_episodes(conn,cursor)
    pop_episode(conn,cursor,path)
    cursor.close()

            
            
