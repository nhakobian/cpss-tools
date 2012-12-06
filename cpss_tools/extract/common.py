def obsblockgen(numb, array, freq, name):
    #filter out all non-alphanumeric characters from name
    filtername = ""
    for letter in name:
        if (letter.isalnum() == True):
            filtername = filtername + letter

    #filter out everything after the . in freq. max 3 chars
    filterfreq = ""
    for digit in freq:
        if (digit == "."):
            break
        else:
            filterfreq = filterfreq + digit
    filterfreq = filterfreq[0:3]

    obsblockname = str(numb) + array + "_" + filterfreq + filtername[0:6]
    return obsblockname

try:
    from string import Template
except ImportError:
    from stringtemplate import Template

category_map = { 
    #'' : 'GALACTIC',
    #'' : 'COMET',
    #'' : 'EXTRAGALACTIC'
    #'' : 'OTHER',
    'Planetary'                       : 'PLANET',
    'Solar'                           : 'SOLAR',
    'Stellar'                         : 'STELLAR',
    'High-mass Star Formation'        : 'HIGH_MASS_SFR',
    'Low-mass Star Formation'         : 'LOW_MASS_SFR',
    'Chemistry / Interstellar Medium' : 'CHEMISTRY-ISM',
    'Galaxies - Detection'            : 'GALAXY_DETECTION',
    'Galaxies - Mapping'              : 'GALAXY_MAPPING',
    'Cosmology'                       : 'COSMOLOGY',
    'Other Galactic'                  : 'OTHER_GALACTIC',
    'Other Extragalactic'             : 'OTHER_EXTRAGALACTIC',
    }

XMLTemplate = Template("""<project>
  <projectID>${carmaid}</projectID>
  <callForProposals term="${term}"/>
  <title>${title}</title>
  <investigators>
    <numberOfInvestigators>${nois}</numberOfInvestigators>
${PI}${CoIs}  </investigators>
  <targetOfOpportunity>${toe}</targetOfOpportunity>
  <keyProject>${key_project}</keyProject>
  <category>${scientific_category}</category>
  <abstract>${abstract}</abstract>
${Obsblocks}</project>
""")

# Check recieverBand
# Why is isFlex filled with a variable called fill?
ObsblockTemplate = Template("""  <obsblock>
    <obsblockID>${obsblock}</obsblockID>
    <observationType>${observation_type}</observationType>
    <recieverBand>${frequency_band}</recieverBand>
    <restFrequency>${rest_frequency}</restFrequency>
    <arrayConfiguration>${array_config}</arrayConfiguration>
    <isFlex>${fill}</isFlex>
    <subObsblock>
      <trial>
        <numberOfPointings>${numb_fields}</numberOfPointings>
        <target>
          <molecule>${species}</molecule>
          <transition></transition>
        </target>
        <objects>
          <source>
            <sourceName>${name}</sourceName>
            <RA>${ra}</RA>
            <DEC>${dec}</DEC>
            <selfcalibratable>${self_cal}</selfcalibratable>
          </source>
        </objects>
        <constraints>
          <imgVsSnr value="${imgvssnr}"/>
        </constraints>
      </trial>
    </subObsblock>
  </obsblock>
""")

PITemplate = Template("""    <PI>
      <name>${name}</name>
      <email>${email}</email>
      <affiliation>${affil}</affiliation>
      <US>${us}</US>
    </PI>
""")

CoITemplate = Template("""    <CoI>
      <name>${name}</name>
      <email>${email}</email>
      <affiliation>${affil}</affiliation>
      <US>${us}</US>
    </CoI>
""")
