# Create tables for title,movies,tvSeries and genres


def create_title(c):
    print("creating titles")
    c.execute('''
        CREATE Table titles(
            tconst text not null primary key,
	        fType text not null,
	        title text not null,
	        originaltitle text not null,
            startYear INTEGER
        );
    ''')

def create_movies(c):
    print("creating movies")
    c.execute('''
        CREATE Table movies(
            tconst text not null primary key,
            runTime INTEGER,
            
            FOREIGN KEY (tconst) REFERENCES titles(tconst) ON DELETE CASCADE ON UPDATE CASCADE
        );
    ''')

def create_tvSeries(c):
    print("creating tvSeries")
    c.execute('''
        CREATE Table tvSeries(
            tconst text not null primary key,
            endYear INTEGER,

            FOREIGN KEY (tconst) REFERENCES titles(tconst) ON DELETE CASCADE ON UPDATE CASCADE);
    ''')

def create_genres(c):
    print("creating genres")
    c.execute('''
        CREATE Table genres(
            tconst text not null,
            genre text,

            FOREIGN KEY (tconst) REFERENCES titles(tconst) ON DELETE CASCADE ON UPDATE CASCADE);
    ''')


def create(connection):
    cursor = connection.cursor()
    #create
    create_title(cursor)
    create_movies(cursor)
    create_tvSeries(cursor)
    create_genres(cursor)

    connection.commit()
    cursor.close()