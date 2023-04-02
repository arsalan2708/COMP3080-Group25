import pyodbc #library required to run this
from build import create_projects as p, pop_projects as pp
from build import people , episodes, link, rate


# serverName = "DaaPC\SQLEXPRESS"  #example of my server name
# dbName =  "testDB"               #example name of my database
dataPath = "../../dataset/"

def buildDB(conn):
    p.create(conn)
    pp.populate(conn,dataPath)
    people.build(conn,dataPath)
    episodes.build(conn,dataPath)
    link.build(conn,dataPath)
    rate.build(conn,dataPath)


def run(attempt=0):
    serverName = input("Please provide the SQL server name:\t")
    dbName =  input(f"Provide DataBase name that is in '{serverName}':\t")
    
    try:
        conn = pyodbc.connect('Driver={SQL Server};'f'Server={serverName};'
        f'Database={dbName};''Trusted_Connection=yes;')
        print("connection Successfull!")
        buildDB(conn)
        conn.close() #close connection
    except:   
        if attempt>=3:
            print("Due to repeated failure to connect, ending program...")
        else:
            print("Failed to connect. Please try again!")
            run(attempt+1)



run()
print("\nprogram execution complete!")
