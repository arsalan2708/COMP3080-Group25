# import pyodbc #library required to run this
import sqlite3
# from build import create_projects as p, pop_projects as pp
# from build import people , episodes, link, rate

dataPath = "../../"

def buildDB(conn):
    p.create(conn)
    pp.populate(conn,dataPath+'dataset/')
    people.build(conn,dataPath+'dataset/')
    episodes.build(conn,dataPath+'dataset/')
    link.build(conn,dataPath+'dataset/')
    rate.build(conn,dataPath+'dataset/')


def run():
    conn = sqlite3.connect(dataPath+'database/database.db')
    conn.execute("PRAGMA foreign_keys = 1") #TURN ON foreign key support
    print("connection Successfull!")
    buildDB(conn)
    conn.close() #close connection
  


run()

# conn = sqlite3.connect(dataPath+'database/database.db')
# test = conn.cursor()
# g = test.execute("select distinct genre from genres order by genre")

# for d in g:
#     print(d[0])


print("\nprogram execution complete!")
