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
    'esgf-node.ipsl.upmc.fr',
    'esg-dn1.nsc.liu.se',
    'esgdata.gfdl.noaa.gov',
    'esgf.nccs.nasa.gov'
]

ESGF_SEARCH_SUFFIX = '/esg-search/search'

DATA_DIRECTORY = '/tmp'
