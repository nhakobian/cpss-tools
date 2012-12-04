#! /usr/bin/python
import sys
sys.path.append(sys.path[0] + '/../db')

import hashlib
import cpssdb

db = None

def proposals_get(user_fr):
    # Find all proposals (submitted or not) by user in each of the systems
    # (main, ddt, summerschool)

    cursor = db.dictcursor()
    cursor.execute("""SELECT `proposalid`, `carmaid`, `user`
                      FROM   `proposals`
                      WHERE  `user`='%s'
                      ORDER BY `carmaid`""" % user_fr)
    main = cursor.fetchall()
    cursor.close()

    cursor = db.dictcursor()
    cursor.execute("""SELECT `proposalid`, `carmaid`, `user`
                      FROM   `ddt_proposals`
                      WHERE  `user`='%s'
                      ORDER BY `carmaid`""" % user_fr)
    ddt = cursor.fetchall()
    cursor.close()

    cursor = db.dictcursor()
    cursor.execute("""SELECT `proposalid`, `carmaid`, `user`
                      FROM   `cs_proposals`
                      WHERE  `user`='%s'
                      ORDER BY `carmaid`""" % user_fr)
    cs = cursor.fetchall()
    cursor.close()
    
    return (main, ddt, cs)


def user_exists(name):
    cursor = db.cursor()
    cursor.execute("""SELECT name, email 
                      FROM `users`
                      WHERE `email`='%s'
                      LIMIT 1""" % name)

    result = cursor.fetchone()
    cursor.close()
    return result

def barf(string=None):
    global db
    if db != None:
        #print "Closing database connection..."
        db.close()
        db = None

    if string != None:
        print string
        sys.exit()
    else:
        raise Exception("Unspecified error...quitting")

def start(fr, to, conf=None):
    global db 

    print "\nchange_email.py - CPSS Change username/merge users tool v1.\n"

    if fr == to:
        barf("Source and destination user names cannot be the same.")

    db = cpssdb.cpssdb()
    
    # See if from user exists:
    if conf == "nousercheck":
        # Flag to skip the from user check. Used to clean up orphaned
        # proposals. Flags to skip user name change at the end (because
        # this doesnt make sense if the proposal has been orphaned).
        #
        # WARNING: This CAN orphan a proposal if the target user does
        # not exist.
        print "Skipping from user check. Using: <" + fr +">"
        user_from = ['', fr]
    else:
        user_from = user_exists(fr)
        if user_from == None:
            barf("Source user does not exist.")
        else:
            print "Source user:\t\t" + user_from[0] + " <" + user_from[1] + ">"

    # See if to user exists:
    user_to = user_exists(to)
    if (user_to == None) and (conf != "nousercheck"):
        user_to = [user_from[0], to]
        merge = False
        print "Target user:\t\t" + user_to[0] + " <" + user_to[1] + ">"
        usermod = True
    elif (user_to == None) and (conf == "nousercheck"):
        user_to = [user_from[0], to]
        merge = False
        print "Target user:\t\t" + user_to[0] + " <" + user_to[1] + ">"
        print "WARNING: The proposals moved below WILL be orphaned."
        usermod = False
    else:
        if conf == "nousercheck":
            usermod = False
            print "WARNING: This operation will leave source user intact."
            merge = False
        else:
            usermod = True
            merge = True
        print "Merge into user:\t" + user_to[0] + " <" + user_to[1] + ">"

    # Retrieve lists of proposals:
    (main, ddt, cs) = proposals_get(user_from[1])

    # If merge is true do force check:
    if merge == True:
        print "\nMerging is an irreverseable action."
        print "The following actions will occur if your proceed:"
        print "\nThe following proposals will be moved to the user <" + user_to[1] + ">:"

        for i in main:
            print "\tMain: " + str(i['proposalid']) + "\t" + str(i['carmaid'])
        for i in ddt:
            print "\t DDT: " + str(i['proposalid']) + "\t" + str(i['carmaid'])
        for i in cs:
            print "\t  CS: " + str(i['proposalid']) + "\t" + str(i['carmaid'])
            
        print "\nThe following user will be deleted: <" + user_from[1] + ">"

        user_hash = hashlib.md5(user_from[1]+user_to[1]).hexdigest()[0:5]

        if conf == None:
            print "\nTo confirm this operation, please rerun this script with"
            print "the following command line:\n"
            print "  ./change_email.py " + user_from[1] + " " + user_to[1] + " " + user_hash
            barf("")
        elif conf != user_hash:
            print "\nERROR: The entered confirmation code is not correct."
            print "To confirm this operation, please rerun this script with"
            print "the following command line:\n"
            print "  ./change_email.py " + user_from[1] + " " + user_to[1] + " " + user_hash
            barf("")

    print
    print "  Main proposal system"
    print "  ===================="
    if len(main) == 0:
        print "  No proposals found"
    # Loop over all main results, changing output
    for result in main:
        cursor = db.dictcursor()
        print "  " + str(result['carmaid']) + "\t<" + str(result['proposalid']) + \
            ">\t (" + str(result['user']) + ") --> (" + user_to[1] + ")"
        cursor.execute("""UPDATE `proposals`
                          SET    `user`='%s'
                          WHERE  `proposalid`='%s'
                          LIMIT  1""" % (user_to[1], result['proposalid']))
        cursor.close()


    print
    print "  DDT proposal system"
    print "  ==================="
    if len(ddt) == 0:
        print "  No proposals found"
    # Loop over all results, changing output
    for result in ddt:
        cursor = db.dictcursor()
        print "  " + str(result['carmaid']) + "\t<" + str(result['proposalid']) + \
            ">\t (" + str(result['user']) + ") --> (" + user_to[1] + ")"
        cursor.execute("""UPDATE `ddt_proposals`
                          SET    `user`='%s'
                          WHERE  `proposalid`='%s'
                          LIMIT  1""" % (user_to[1], result['proposalid']))
        cursor.close()

    print
    print "  Summerschool proposal system"
    print "  ============================"
    if len(cs) == 0:
        print "  No proposals found"
    # Loop over all results, changing output
    for result in cs:
        cursor = db.dictcursor()
        print "  " + str(result['carmaid']) + "\t<" + str(result['proposalid']) + \
            ">\t (" + str(result['user']) + ") --> (" + user_to[1] + ")"
        cursor.execute("""UPDATE `cs_proposals`
                          SET    `user`='%s'
                          WHERE  `proposalid`='%s'
                          LIMIT  1""" % (user_to[1], result['proposalid']))
        cursor.close()

    if (usermod == True) and (merge == False):
        # Change the username in the users table to the new username.
        cursor = db.cursor()
        print "\n  Changing <"+user_from[1]+"> to <" + user_to[1]+ ">"
        cursor.execute("""UPDATE `users`
                          SET    `email`='%s'
                          WHERE  `email`='%s'
                          LIMIT 1""" % (user_to[1], user_from[1]))
        cursor.close()
    elif (usermod == True) and (merge == True):
        # DELETE the old username in the users table to the new username.
        cursor = db.cursor()
        print "\n  Deleting user <"+user_from[1]+">"
        cursor.execute("""DELETE FROM `users`
                          WHERE  `email`='%s'
                          LIMIT 1""" % (user_from[1]))
        cursor.close()

    print "\nAll operations are complete."
    print "Run 'orphan_all.py' to check no proposals were orphaned."
    print "Run find_prop.py on the source and destination users to verify operations."

    db.close()
    db = None

if __name__ == "__main__":
    if len(sys.argv) == 4:
        start(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        start(sys.argv[1], sys.argv[2])
