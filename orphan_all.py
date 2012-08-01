#! /usr/bin/python
# Checks to see if there are any orphaned proposals (proposals whose user
# is not registered with the system).
import cpssdb
import md5
import sys


def start():
    Database = cpssdb.cpssdb()
    
    cursor = Database.cursor()
    cursor.execute("""SELECT prop.proposalid, prop.carmaid, prop.user
                      FROM proposals as prop
                      WHERE prop.user NOT IN(SELECT email FROM users)
                      ORDER BY prop.carmaid""")

    while (1):
        result = cursor.fetchone()
        if (result != None):
            print result
        else:
            break

    cursor.close()
    #ddt
    cursor = Database.cursor()
    cursor.execute("""SELECT prop.proposalid, prop.carmaid, prop.user
                      FROM ddt_proposals as prop
                      WHERE prop.user NOT IN(SELECT email FROM users)
                      ORDER BY prop.carmaid""")

    while (1):
        result = cursor.fetchone()
        if (result != None):
            print result
        else:
            break

    cursor.close()
    #summerschool
    cursor = Database.cursor()
    cursor.execute("""SELECT prop.proposalid, prop.carmaid, prop.user
                      FROM cs_proposals as prop
                      WHERE prop.user NOT IN(SELECT email FROM users)
                      ORDER BY prop.carmaid""")

    while (1):
        result = cursor.fetchone()
        if (result != None):
            print result
        else:
            break

    cursor.close()
    Database.close()

if __name__ == "__main__":
    start()
