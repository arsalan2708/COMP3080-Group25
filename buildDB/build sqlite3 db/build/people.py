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
        connection.commit()
    cursor.close()


def createPeople(connection,path):
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE people(
        nconst text not null primary key,
        name text not null,
        birthYear int not null,
        deathYear int);''')
    connection.commit()
    cursor.close()
    print("People Created ... proceeding to populate")
    popPeople(connection,path)


def popProfession(connection,path):
    cursor = connection.cursor()
    with open(path+"/profession.tsv") as f:
        f.readline()
        for data in f:
            data = data.strip().split("\t")
            cursor.execute('INSERT INTO profession VALUES(?,?);',data)
        connection.commit()
    cursor.close()


def createProfession(connection,path):
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE profession(
    nconst text not null,
    profession text not null,
    
    FOREIGN KEY (nConst) REFERENCES people(nconst) ON DELETE CASCADE ON UPDATE CASCADE
    );''')

    connection.commit()
    cursor.close()
    print("Professions Created ... proceeding to hire")
    popProfession(connection,path)


def build(connection,path):
    createPeople(connection,path)
    createProfession(connection,path)
