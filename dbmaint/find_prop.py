#! /usr/bin/python
# Find all proposals by a particular user.
import sys
sys.path.append(sys.path[0] + '/../db')

import cpssdb

def start(emails):
    string = "IN('" + "', '".join(emails) + "')"

    Database = cpssdb.cpssdb()
    
    #main
    cursor = Database.cursor()
    cursor.execute("""SELECT * 
                      FROM (SELECT * FROM `proposals` UNION 
                            SELECT * FROM `cs_proposals` UNION 
                            SELECT * FROM `ddt_proposals`) AS t1
                      WHERE `t1`.`user` %s
                      ORDER BY `t1`.`carmaid`""" % string)

    while (1):
        result = cursor.fetchone()
        if (result != None):
            print result
        else:
            break

    cursor.close()
    Database.close()

if __name__ == "__main__":
    start(sys.argv[1:])
