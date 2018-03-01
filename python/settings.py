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

    HOME_DIR = os.environ['HOME']

    '''
    Open Targets Scoring Matrices
    '''

    DRAFT_SCORE_FILE_URLS = dict(
        datasource_scores='https://storage.googleapis.com/biodata-west-hackathon/draft/matrix_datasources_17.12.csv',
        datatype_scores='https://storage.googleapis.com/biodata-west-hackathon/draft/matrix_datatypes_17.12.csv',
    )

    VERSION1_SCORE_FILES = dict(
        output_datasource_scores=os.path.join(os.path.sep, HOME_DIR,'gene_disease_associations_datasource.csv'),
        #output_datasource_scores_nodrugs = os.path.join(os.path.sep, HOME_DIR, 'gene_disease_associations_datasource_nodrugs.csv'),
        output_datatype_scores = os.path.join(os.path.sep, HOME_DIR, 'gene_disease_associations_datatype.csv'),
        #output_datatype_scores_nodrugs = os.path.join(os.path.sep, HOME_DIR,'gene_disease_associations_datatype_nodrugs.csv')

    )

    VERSION2_SCORE_FILES = dict(
        output_datasource_scores=os.path.join(os.path.sep, HOME_DIR, 'gene_disease_associations_datasource_with_expression.csv'),
        output_datatype_scores=os.path.join(os.path.sep, HOME_DIR, 'gene_disease_associations_datatype_with_expression.csv'),
    )

    MERGED_FILES = dict(
        output_datasource_scores=os.path.join(os.path.sep, HOME_DIR, 'gene_expression_disease_associations_datasource.csv'),
        output_datasource_scores_nodrugs=os.path.join(os.path.sep, HOME_DIR,
                                                      'gene_expression_disease_associations_datasource_nodrugs.csv'),
        output_datatype_scores=os.path.join(os.path.sep, HOME_DIR, 'gene_disease_associations_datatype.csv'),
        output_datatype_scores_nodrugs=os.path.join(os.path.sep, HOME_DIR,
                                                    'gene_expression_disease_associations_datatype_nodrugs.csv'),
        output_datasource_scores_expression=os.path.join(os.path.sep, HOME_DIR, 'gene_expression_disease_associations_datasource_v2.csv'),
    )

    GENE_ANNOTATION_FILES = dict(
        hgnc_mappings='https://storage.googleapis.com/biodata-west-hackathon/draft/hgnc_mapping.csv',
        go_annotations='https://storage.googleapis.com/biodata-west-hackathon/draft/human_goa.csv',
        protein_classes='https://storage.googleapis.com/biodata-west-hackathon/draft/human_protein_classes.csv',
        qtq=os.path.join(os.path.sep, HOME_DIR,'QTQ_targetevidence_31Jan2018.csv'),
        output_gene_info=os.path.join(os.path.sep, HOME_DIR,'gene_info.csv'),
        output_gene_info_qtq=os.path.join(os.path.sep, HOME_DIR,'gene_info_qtq.csv'),
    )

    GENE_TISSUE_EXPRESSION = dict(
        gtex='https://storage.googleapis.com/biodata-west-hackathon/draft/EFO_MeSH_GTExTissue_Genes_14Feb2018_list.txt',
        disease_location='https://storage.googleapis.com/biodata-west-hackathon/draft/disease_locations.txt',
        output_tissue_expression=os.path.join(os.path.sep, HOME_DIR,'gene_disease_gtex_tissue_expression.csv'),
        output_tissue_expression_withscore=os.path.join(os.path.sep, HOME_DIR,'gene_disease_gtex_tissue_expression_v2.csv'),
        output_disease_location = os.path.join(os.path.sep, HOME_DIR, 'disease_uberon_location.csv')
    )


    PHARMAPROJECTS = dict(
        original_file=os.path.join(os.path.sep, HOME_DIR,'Pprojects_8_5_2017_for_BDW.csv'),
        output_pharmaprojects=os.path.join(os.path.sep, HOME_DIR,'Pprojects_drugs.csv'),
    )


    HGNC_FILE = ''