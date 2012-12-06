from cpss_tools import db

import inst
import common
import shutil

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

        self.authors_extract(proposals)
        # export
        # obsblock
        self.password_extract(proposals)
        self.pdf_extract(proposals)
        # proposal
        pass
    
    def xml_extract(self, cycle_type, start, end):
        pass
        
    def password_extract(self, proposals):
        output = open('./password.xml', 'w')

        for prop in proposals:
            output.write("<projectID>" + prop['carmaid'] + 
                         "</projectID><passWord>" + prop['carmapw'] + 
                         "</passWord>\n")
        output.close()
        print "Extracted passwords for %s proposals." % len(proposals)

    def pdf_extract(self, proposals):
        pdfdir = self.db.filedir + '/pdf/'
        for prop in proposals:
            shutil.copy(pdfdir + str(prop['proposalid']) + '.pdf', 
                        './' + prop['carmaid'] + '.pdf')
        print "Extracted pdf files for %s proposals." % len(proposals)

    def authors_extract(self, proposals):
        output = open('./authors.csv', 'w')
        output.write("""\"Carma ID","Author Number","Name","E-mail","Phone Number","Institution","Thesis","Graduate Student"\n""")

        for prop in proposals:
            authors = self.db.authors_by_proposal(prop['author'], 
                                                  prop['proposalid'])
            for auth in authors:
                tmp = [prop['carmaid'], auth['numb'], auth['name'], 
                       auth['email'], auth['phone'], auth['institution'], 
                       auth['thesis'], auth['grad']]
                for i in xrange(len(tmp)):
                    tmp[i] = """\"%s\"""" % tmp[i]
                output.write(','.join(tmp))
                output.write('\n')
        output.close()
        print "Extracted author information from %s proposals." % len(proposals)



