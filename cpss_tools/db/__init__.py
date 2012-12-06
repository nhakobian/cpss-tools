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
        self.literal = self.db.literal
        self.filedir = dbconfig.data_dir

    def dictcursor(self):
        return self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    def cursor(self):
        return self.db.cursor()

    def close(self):
        return self.db.close()

    def proposals_by_cyclename(self, cyclename):
        cursor = self.dictcursor()
        
        cursor.execute("""SELECT * 
                          FROM `proposals`, `cycles`
                          WHERE `proposals`.`cyclename`=`cycles`.`cyclename`
                          AND `proposals`.`cyclename`=%(cyclename)s
                          AND `proposals`.`carmaid` IS NOT NULL
                          ORDER BY `proposals`.`carmaid`""" %
                       {'cyclename' : self.literal(cyclename)})
        res = cursor.fetchall()
        cursor.close()

        return res

    def authors_by_proposal(self, table, proposalid):
        cursor = self.dictcursor()

        cursor.execute("""SELECT *
                          FROM %(table)s
                          WHERE `proposalid`=%(prop)s
                          ORDER BY `numb`""" %
                       { 'table' : table,
                         'prop'  : self.literal(proposalid)})
        res = cursor.fetchall()
        cursor.close()
        return res

    def propinfo_by_proposal(self, table, proposalid):
        cursor = self.dictcursor()

        cursor.execute("""SELECT *
                          FROM %(table)s
                          WHERE `proposalid`=%(prop)s
                          LIMIT 1""" %
                       { 'table' : table,
                         'prop'  : self.literal(proposalid)})
        res = cursor.fetchone()
        cursor.close()
        return res

    def sources_by_proposal(self, table, proposalid):
        cursor = self.dictcursor()

        cursor.execute("""SELECT *
                          FROM %(table)s
                          WHERE `proposalid`=%(prop)s
                          ORDER BY `numb`""" %
                       { 'table' : table,
                         'prop'  : self.literal(proposalid)})
        res = cursor.fetchall()
        cursor.close()
        return res
