''' populate projects such as Titles
                              movies , tvSeries, genres'''

def populate(connection,path):
    cursor = connection.cursor()
    with open(path+"title.tsv") as f:
        f.readline()
        for data in f:
            data = data.strip().split("\t")
            data[4] = int(data[4]) #start year
            data[5] = None if (data[5] == 0 or data[5]=='') else int(data[5]) #endyear
            data[6] = int(data[6]) #runTime
            popTitle(cursor, data[:5])
            if data[1]=='movie': popMovie(cursor,(data[0],data[6]))
            if data[1]=='tvSeries': poptvSeries(cursor,(data[0],data[5]))
            popGenre(cursor, (data[0],data[7]))
            connection.commit()
    cursor.close()


def popTitle(c, data):
    sqlInsert = f'''INSERT INTO titles Values (?,?,?,?,?); '''
    c.execute(sqlInsert,data)

def popMovie(c, data):
    sqlInsert = f'''INSERT INTO movies Values (?,?); '''
    c.execute(sqlInsert,data)


def poptvSeries(c, data):
    sqlInsert = f'''INSERT INTO tvSeries Values (?,?); '''
    c.execute(sqlInsert,data)

def popGenre(c, data):
    sqlInsert = f'''INSERT INTO genres Values (?,?); '''
    for genre in data[1].strip('"').split(','):
        c.execute(sqlInsert,(data[0],genre))
    
        
