from database import startDb

if __name__ == '__main__':
    con = startDb.connectToDb('./database/database.sqlite3')
    startDb.start_db(con,'./database/MdCharas.csv','urls.csv')