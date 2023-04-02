# create people table and profession table  and populate it


def popPeople(connection,path):
    cursor = connection.cursor()
    sqlInput = '''insert into people values(?,?,?,?)'''
    with open(path+"people.tsv") as f:
        f.readline()
        for data in f:
            data = data.strip().split("\t")
            data[2] = None if data[2] == 0 or data[2] == '' else int(
                data[2])  # casting birthYear to int
            if len(data)>3:data[3] = int(data[3])
            else: data.append(None)
            cursor.execute(sqlInput, data)
        cursor.commit()
    cursor.close()


def createPeople(connection,path):
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE people(
        nconst varchar(30) not null primary key,
        name varchar(150) not null,
        birthYear int not null,
        deathYear int);''')
    cursor.commit()
    cursor.close()
    print("People Created ... proceeding to populate")
    popPeople(connection,path)


def popProfession(connection,path):
    cursor = connection.cursor()
    with open(path+"profession.tsv") as f:
        f.readline()
        for data in f:
            data = data.strip().split("\t")
            cursor.execute('INSERT INTO profession VALUES(?,?);',data)
        cursor.commit()
    cursor.close()


def createProfession(connection, path):
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE profession(
    nconst varchar(30) not null,
    profession varchar(100) not null,
    
    FOREIGN KEY (nConst) REFERENCES people(nconst) ON DELETE CASCADE ON UPDATE CASCADE
    );''')

    cursor.commit()
    cursor.close()
    print("Professions Created ... proceeding to hire")
    popProfession(connection,path)


def build(connection,path):
    createPeople(connection,path)
    createProfession(connection,path)
