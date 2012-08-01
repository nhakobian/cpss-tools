#! /usr/bin/python
# Display information about a particular CARMA proposal id.
import sys
sys.path.append(sys.path[0] + '/../db')

import cpssdb

def start(carmaid):
    Database = cpssdb.cpssdb()
    
    cursor = Database.cursor()
    sql = ("""SELECT * 
                      FROM (SELECT * FROM `proposals` UNION 
                            SELECT * FROM `cs_proposals` UNION 
                            SELECT * FROM `ddt_proposals`) AS t1, `users`
                      WHERE t1.carmaid='%s' AND
                            `t1`.`user`=`users`.`email`""" % carmaid)

    cursor.execute(sql)
    while (1):
        result = cursor.fetchone()
        if (result != None):
            print result
        else:
            break

    cursor.close()
    Database.close()


if __name__ == "__main__":
    start(sys.argv[1])
