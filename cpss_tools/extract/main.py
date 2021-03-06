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
        self.xml_extract(proposals)
        self.obsblock_extract(proposals)
        self.password_extract(proposals)
        self.pdf_extract(proposals)
        self.proposal_extract(proposals)
    
    def xml_extract(self, proposals):
        # author information by proposal
        authors = {}
        for prop in proposals:
            aut = self.db.authors_by_proposal(prop['author'], 
                                                  prop['proposalid'])
            authors[prop['carmaid']] = aut

        # Extract propinfo sorted by proposal
        propinfo = {}
        for prop in proposals:
            info = self.db.propinfo_by_proposal(prop['proposal'],
                                                    prop['proposalid'])
            propinfo[prop['carmaid']] = info

        sources = self.sourceinfo(proposals)

        output = open('export.xml', 'w')
        output_strip = open('export_stripped.xml', 'w')

        for prop in proposals:
            pi_data = authors[prop['carmaid']][0]
            aut_data = authors[prop['carmaid']][1:]
            prop_data = propinfo[prop['carmaid']]
            source_data = sources[prop['carmaid']]

            nois = len(aut_data)

            PI = common.PITemplate.substitute(name=pi_data['name'], 
                   email=pi_data['email'], affil=pi_data['institution'], 
                   us=inst.isus(pi_data['institution']))

            CoIs = ""
            for coi in aut_data:
                CoIs += common.CoITemplate.substitute(name=coi['name'], 
                          email=coi['email'], affil=coi['institution'], 
                          us=inst.isus(coi['institution']))
    
            Obsblocks = ""
            for source in source_data:
                if source['imaging'] == 'Imaging':
                    imgsnr = 'IMG'
                elif source['imaging'] == 'SNR':
                    imgsnr = 'SNR'
                else:
                    imgsnr = ''

                prop['frequency_band'] = ''
            
                Obsblocks += common.ObsblockTemplate.substitute(
                    obsblock = source['obsblock'],
                    frequency_band = prop['frequency_band'],
                    array_config = source['config'],
                    fill = source['flexha'],
                    numb_fields = source['numb_fields'],
                    species = source['species'],
                    name = source['name'],
                    ra = source['ra'],
                    dec = source['dec'],
                    self_cal = source['self_cal'],
                    rest_frequency = source['corr_frequency'],
                    observation_type = source['observation_type'],
                    imgvssnr = imgsnr,
                    )

            # Grab and filter the abstract
            prop_data['abstract'] = prop_data['abstract'].replace('\n', ' ')
            prop_data['abstract'] = prop_data['abstract'].replace('\r', '')
            prop_data['abstract'] = prop_data['abstract'].replace('\\', '\\\\')
            prop_data['abstract'] = prop_data['abstract'].replace('$', '\$')
            prop_data['abstract'] = prop_data['abstract'].replace('"', '\\"')
            prop_data['abstract'] = prop_data['abstract'].replace("'", "\\'")

            xml_proposal = common.XMLTemplate.substitute(
                carmaid = prop['carmaid'],
                term = prop['cyclename'],
                title = prop_data['title'],
                nois = nois,
                PI = PI,
                CoIs = CoIs,
                key_project = prop_data['key_project'],
                toe = prop_data['toe'],
                scientific_category=common.category_map[prop_data['scientific_category']],
                abstract = prop_data['abstract'],
                Obsblocks = Obsblocks)
            
            xml_strip = xml_proposal.replace('\n', '')
            xml_strip = xml_strip.replace('>  <', '><')
            xml_strip = xml_strip.replace('>    <', '><')
            xml_strip = xml_strip.replace('>      <', '><')
            xml_strip = xml_strip.replace('>        <', '><')
            xml_strip = xml_strip.replace('>          <', '><')
            xml_strip = xml_strip.replace('>            <', '><')

            output.write(xml_proposal)
            output_strip.write(xml_strip)
            output_strip.write('\n')

        output.close()
        output_strip.close()

        print "Exported XML data from %s proposals." % len(proposals)
    
    def sourceinfo(self, proposals):
        # Extract sourceinfo with obsblockname
        sources = {}
        for prop in proposals:
            sources[prop['carmaid']] = []
            sinfo = self.db.sources_by_proposal(prop['source'],
                                                  prop['proposalid'])
            for s in sinfo:
                if (s['hrs_a'] != '0') and (s['hrs_a'] != None):
                    tmp = s.copy()
                    tmp['config'] = 'A'
                    tmp['hours'] = s['hrs_a']
                    tmp['obsblock'] = common.obsblockgen(tmp['numb'], 
                      tmp['config'], tmp['corr_frequency'], tmp['name'])
                    sources[prop['carmaid']].append(tmp)
                if (s['hrs_b'] != '0') and (s['hrs_b'] != None):
                    tmp = s.copy()
                    tmp['config'] = 'B'
                    tmp['hours'] = s['hrs_b']
                    tmp['obsblock'] = common.obsblockgen(tmp['numb'], 
                      tmp['config'], tmp['corr_frequency'], tmp['name'])
                    sources[prop['carmaid']].append(tmp)
                if (s['hrs_c'] != '0') and (s['hrs_c'] != None):
                    tmp = s.copy()
                    tmp['config'] = 'C'
                    tmp['hours'] = s['hrs_c']
                    tmp['obsblock'] = common.obsblockgen(tmp['numb'], 
                      tmp['config'], tmp['corr_frequency'], tmp['name'])
                    sources[prop['carmaid']].append(tmp)
                if (s['hrs_d'] != '0') and (s['hrs_d'] != None):
                    tmp = s.copy()
                    tmp['config'] = 'D'
                    tmp['hours'] = s['hrs_d']
                    tmp['obsblock'] = common.obsblockgen(tmp['numb'], 
                      tmp['config'], tmp['corr_frequency'], tmp['name'])
                    sources[prop['carmaid']].append(tmp)
                if (s['hrs_e'] != '0') and (s['hrs_e'] != None):
                    tmp = s.copy()
                    tmp['config'] = 'E'
                    tmp['hours'] = s['hrs_e']
                    tmp['obsblock'] = common.obsblockgen(tmp['numb'], 
                      tmp['config'], tmp['corr_frequency'], tmp['name'])
                    sources[prop['carmaid']].append(tmp)
                if (s['hrs_sh'] != '0') and (s['hrs_sh'] != None):
                    tmp = s.copy()
                    tmp['config'] = 'SH'
                    tmp['hours'] = s['hrs_sh']
                    tmp['obsblock'] = common.obsblockgen(tmp['numb'], 
                      tmp['config'], tmp['corr_frequency'], tmp['name'])
                    sources[prop['carmaid']].append(tmp)
                if (s['hrs_sl'] != '0') and (s['hrs_sl'] != None):
                    tmp = s.copy()
                    tmp['config'] = 'SL'
                    tmp['hours'] = s['hrs_sl']
                    tmp['obsblock'] = common.obsblockgen(tmp['numb'], 
                      tmp['config'], tmp['corr_frequency'], tmp['name'])
                    sources[prop['carmaid']].append(tmp)
        return sources

    def obsblock_extract(self, proposals):
        # PI information by proposal
        pis = {}
        for prop in proposals:
            authors = self.db.authors_by_proposal(prop['author'], 
                                                  prop['proposalid'])
            pis[prop['carmaid']] = authors[0]

        # Extract propinfo sorted by proposal
        propinfo = {}
        for prop in proposals:
            info = self.db.propinfo_by_proposal(prop['proposal'],
                                                    prop['proposalid'])
            propinfo[prop['carmaid']] = info

        sources = self.sourceinfo(proposals)
    
        output = open('obsblocks.csv', 'w')
        output.write("""\"Carma ID","Obsblock Name","Title","Date","PI Name","PI E-mail","PI Institution","Target of Opportunity","Scientific Category","Help Required","Source Name","RA","DEC","Frequency of Observation","Array","Hours Requested","Observation Type","Number of Mosaic Fields","Species or Transition Name","Can Self-Calibrate","Imag/SNR","Flexible Hour Angle\"\n""")

        for prop in proposals:
            tpi = pis[prop['carmaid']]
            tpropinfo = propinfo[prop['carmaid']]
            tsources = sources[prop['carmaid']]
            
            for s in tsources:
                tmp = [prop['carmaid'], s['obsblock'], tpropinfo['title'],
                       tpropinfo['date'], tpi['name'], tpi['email'], 
                       tpi['institution'], tpropinfo['toe'], 
                       tpropinfo['scientific_category'], 
                       tpropinfo['help_required'], s['name'], s['ra'], 
                       s['dec'], s['corr_frequency'], s['config'], s['hours'],
                       s['observation_type'], s['numb_fields'], s['species'], 
                       s['self_cal'], s['imaging'], s['flexha']]

                for i in xrange(len(tmp)):
                    tmp[i] = """\"%s\"""" % tmp[i]

                output.write(','.join(tmp))
                output.write('\n')
        
        output.close()
        print "Extracted obsblock info for %s proposals." % len(proposals)

    def proposal_extract(self, proposals):
        # PI information by proposal
        pis = {}
        for prop in proposals:
            authors = self.db.authors_by_proposal(prop['author'], 
                                                  prop['proposalid'])
            pis[prop['carmaid']] = authors[0]

        # Extract propinfo sorted by proposal
        propinfo = {}
        for prop in proposals:
            info = self.db.propinfo_by_proposal(prop['proposal'],
                                                    prop['proposalid'])
            propinfo[prop['carmaid']] = info

        # Extract total number of hours per project
        hours = {}
        for prop in proposals:
            sources = self.db.sources_by_proposal(prop['source'],
                                                  prop['proposalid'])
            hours[prop['carmaid']] = 0.0
            for source in sources:
                if source['hrs_a'] != None:
                    hours[prop['carmaid']] += float(source['hrs_a'])
                if source['hrs_b'] != None:
                    hours[prop['carmaid']] += float(source['hrs_b'])
                if source['hrs_c'] != None:
                    hours[prop['carmaid']] += float(source['hrs_c'])
                if source['hrs_d'] != None:
                    hours[prop['carmaid']] += float(source['hrs_d'])
                if source['hrs_e'] != None:
                    hours[prop['carmaid']] += float(source['hrs_e'])
                if source['hrs_sh'] != None:
                    hours[prop['carmaid']] += float(source['hrs_sh'])
                if source['hrs_sl'] != None:
                    hours[prop['carmaid']] += float(source['hrs_sl'])

        output = open('proposals.csv', 'w')
        output.write("""\"Carma ID","Title","Date","PI Name","PI E-mail","PI Institution","Key Project","Target Of Opportunity","Scientific Category","1cm","1mm","3mm","Help Required","Hours"\n""")

        # Collect info and write to file.
        for prop in proposals:
            tpi = pis[prop['carmaid']]
            tpropinfo = propinfo[prop['carmaid']]
            thours = hours[prop['carmaid']]

            tmp = [prop['carmaid'], tpropinfo['title'], tpropinfo['date'],
                   tpi['name'], tpi['email'], tpi['institution'], 
                   tpropinfo['key_project'], tpropinfo['toe'], 
                   tpropinfo['scientific_category'], tpropinfo['1cm'], 
                   tpropinfo['1mm'], tpropinfo['3mm'], 
                   tpropinfo['help_required'], thours]

            for i in xrange(len(tmp)):
                tmp[i] = """\"%s\"""" % tmp[i]

            output.write(','.join(tmp))
            output.write('\n')

        output.close()
        print "Extracted proposal info for %s proposals." % len(proposals)
        
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
