import MySQLdb

import dbconfig

class cpssdb():
    def __init__(self):
        ### Connect to database
        if dbconfig.unix_socket == None:
            db = MySQLdb.connect(host = dbconfig.host,
                                 port = dbconfig.port,
                                 user = dbconfig.user,
                                 passwd = dbconfig.password,
                                 db = dbconfig.database)
        else:
            db = MySQLdb.connect(host = dbconfig.host,
                                 user = dbconfig.user,
                                 passwd = dbconfig.password,
                                 db = dbconfig.database,
                                 unix_socket = dbconfig.unix_socket)           
        self.db = db

    def dictcursor(self):
        return self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    def cursor(self):
        return self.db.cursor()

    def close(self):
        return self.db.close()
