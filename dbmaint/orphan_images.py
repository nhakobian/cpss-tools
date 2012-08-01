#! /usr/bin/python
# Finds if there are any images not associated with a proposal (should not
# happen under normal circumstances).
import sys
sys.path.append(sys.path[0] + '/../db')

import cpssdb

def start():
    Database = cpssdb.cpssdb()
    
    #main
    cursor = Database.dictcursor()
    cursor.execute("""SELECT * FROM `images`WHERE `images`.`proposalid` NOT IN (SELECT `proposalid` FROM `proposals`) """)

    while (1):
        result = cursor.fetchone()
        if (result != None):
            print "%s.%s.gz" % (result['proposalid'], result['numb'])
        else:
            break

    cursor.close()
    Database.close()

if __name__ == "__main__":
    start()
