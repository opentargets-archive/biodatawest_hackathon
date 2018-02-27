import os
import ConfigParser
import uuid
from collections import defaultdict

__copyright__ = "Copyright 2014-2018, Open Targets"
__credits__ = ["Gautier Koscielny"]
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautier.x.koscielny@gsk.com"
__status__ = "Production"

iniparser = ConfigParser.ConfigParser()
iniparser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'env.ini'))

class Config():

    HAS_PROXY = iniparser.has_section('proxy')
    if HAS_PROXY:
        PROXY = iniparser.get('proxy', 'protocol') + "://" + iniparser.get('proxy', 'username') + ":" + iniparser.get('proxy', 'password') + "@" + iniparser.get('proxy', 'host') + ":" + iniparser.get('proxy', 'port')
        PROXY_PROTOCOL = iniparser.get('proxy', 'protocol')
        PROXY_USERNAME = iniparser.get('proxy', 'username')
        PROXY_PASSWORD = iniparser.get('proxy', 'password')
        PROXY_HOST = iniparser.get('proxy', 'host')
        PROXY_PORT = int(iniparser.get('proxy', 'port'))

    CACHE_DIRECTORY = iniparser.get('cache', 'directory')

    '''
    Open Targets Scoring Matrices
    '''

    SCORE_FILE_URLS = dict(
        datasource_scores='https://storage.googleapis.com/biodata-west-hackathon/matrix_datasources_17.12.csv',
        datatype_scores='https://storage.googleapis.com/biodata-west-hackathon/matrix_datatypes_17.12.csv'
    )


    HGNC_FILE = ''