#
# Some license
#
# Author: Stering Baldwin
#         baldwin32@llnl.gov
#


'''Module containing constant parameters for ESGF integration for the ACME Dashboard backend'''

# Default location of ESGF user credentials
ESGF_CREDENTIALS = '~/.esg/credentials.pem'

# List of all current ESGF nodes
NODE_HOSTNAMES = [
    'pcmdi.llnl.gov',
    'esgf-node.jpl.nasa.gov',
    'esgf-index1.ceda.ac.uk',
    'esgf-data.dkrz.de',
    'esg-dn1.nsc.liu.se',
    'esgf-node.ipsl.upmc.fr',
    'esgf.nci.org.au'
    'esg-dn1.nsc.liu.se',
    'esgdata.gfdl.noaa.gov',
    'esgf.nccs.nasa.gov',
    'esg.ccs.ornl.gov'
]

ESGF_SEARCH_SUFFIX = '/esg-search/'

DATA_DIRECTORY = '/tmp'
