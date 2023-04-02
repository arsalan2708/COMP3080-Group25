# Create tables for title,movies,tvSeries and genres


def create_title(c):
    print("creating titles")
    c.execute('''
        CREATE Table titles(
            tconst varchar(30) not null primary key,
	        fType varchar(30) not null,
	        title varchar(max) not null,
	        originaltitle varchar(max) not null,
            startYear int
        );
    ''')
    c.commit()

def create_movies(c):
    print("creating movies")
    c.execute('''
        CREATE Table movies(
            tconst varchar(30) not null,
            runTime int,
            
            FOREIGN KEY (tconst) REFERENCES titles(tconst) ON DELETE CASCADE ON UPDATE CASCADE
        );
    ''')
    c.commit()

def create_tvSeries(c):
    print("creating tvSeries")
    c.execute('''
        CREATE Table tvSeries(
            tconst varchar(30) not null primary key,
            endYear int,

            FOREIGN KEY (tconst) REFERENCES titles(tconst) ON DELETE CASCADE ON UPDATE CASCADE
        );
    ''')
    c.commit()

def create_genres(c):
    print("creating genres")
    c.execute('''
        CREATE Table genres(
            tconst varchar(30) not null,
            genre varchar(35),

            FOREIGN KEY (tconst) REFERENCES titles(tconst) ON DELETE CASCADE ON UPDATE CASCADE
        );
    ''')
    c.commit()


def create(connection):
    cursor = connection.cursor()
    #create
    create_title(cursor)
    create_movies(cursor)
    create_tvSeries(cursor)
    create_genres(cursor)

    cursor.close()