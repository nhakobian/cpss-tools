#! /usr/bin/python
# Checks to see if there are any uploaded justifications not associated with
# a proposal (should not occur under normal circumstances).
import sys
sys.path.append(sys.path[0] + '/../db')

import cpssdb
import os

def start():
    Database = cpssdb.cpssdb()

    cursor = Database.dictcursor()
    cursor.execute("""SELECT `proposalid` FROM `proposals`""")

    just = []
    while (1):
        result = cursor.fetchone()
        if (result != None):
            just.append(result['proposalid'])
        else:
            break

    justfiles = os.listdir('/home/carmaweb/cpss-data/justifications/')
    for i in xrange(len(justfiles)):
        justfiles[i] = int(justfiles[i][:-4])

    for i in justfiles:
        if i not in just:
            print str(i) + '.pdf'

    cursor.close()
    Database.close()

if __name__ == "__main__":
    start()
