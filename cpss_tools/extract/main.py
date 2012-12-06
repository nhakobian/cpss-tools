from cpss_tools import db

import inst
import common

class extract(object):
    def __init__(self):
        self.db = db.cpssdb()

    def extract_by_id(self, cycle_type, start, end):
        pass

    def extract_by_cyclename(self, cyclename):
        # This function searches the list of cycles and extracts the range
        # of proposals in the cycle and calls extract_by_id on the range.

        props = self.db.proposals_by_cyclename(cyclename)

        first = props[0]['carmaid']
        last = props[-1]['carmaid']
        ptype = props[0]['type']
        print "Detected proposal range for %s (%s) is %s - %s" % \
            (cyclename, ptype, first, last)
        self.extract(props)

    def extract(self, proposals):
        # Pass proposal info to each routine. They can call the correct
        # subfunctions to grab each set of data as needed.

        # authors
        # export
        # obsblock
        # password
        # pdf
        # proposal
        pass
    
    def xml_extract(self, cycle_type, start, end):
        pass
        
