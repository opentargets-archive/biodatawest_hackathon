import sys
import os
import pandas as pd
import math
import numpy as np
import logging
import csv
import requests
from contextlib import closing
from settings import Config

__copyright__ = "Copyright 2014-2018, Open Targets"
__credits__ = ["Gautier Koscielny"]
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautier.x.koscielny@gsk.com"
__status__ = "Production"


def read_from_url(url):

    with closing(requests.get(url, stream=True)) as r:
        # decoded_content = download.content.decode('utf-8')

        reader = csv.reader(r.iter_lines(), delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        c = 0
        for row in reader:
            c += 1
            if c > 1:
                print(row)
            if c > 100:
                break

def merge_gene_annotations():

    hgnc_df = pd.read_csv(Config.GENE_ANNOTATION_FILES['hgnc_mappings'], sep='\t')
    hgnc_df['entrez_id'].astype(str)
    hgnc_df['uniprot_id'].astype(str)
    hgnc_df['locus_type'].astype(str)
    hgnc_df['locus_group'].astype(str)
    #print(hgnc_df[:5])

    goa_df = pd.read_csv(Config.GENE_ANNOTATION_FILES['go_annotations'], sep='\t')
    goa_df['entrez_id'].astype(str)
    goa_df['uniprot_id'].astype(str)
    #print(goa_df[:5])
    print("---------------")
    merge1 = pd.merge(hgnc_df, goa_df, how='left', on=['ensembl_gene_id', 'entrez_id', 'uniprot_id'])
    merge1['entrez_id'].astype(str)
    merge1['uniprot_id'].astype(str)
    merge1['go_id'].astype(str)
    merge1['go_label'].astype(str)
    merge1['evidence_type'].astype(str)

    '''
    merge protein classes when they exist
    '''
    protein_classes_df = pd.read_csv(Config.GENE_ANNOTATION_FILES['protein_classes'], sep='\t')
    protein_classes_df['entrez_id'].astype(str)
    protein_classes_df['uniprot_id'].astype(str)
    print(protein_classes_df[:5])
    print("---------------")

    df = pd.merge(merge1, protein_classes_df, how='left', on=['ensembl_gene_id', 'entrez_id', 'uniprot_id'])
    df['entrez_id'].astype(str)
    df['uniprot_id'].astype(str)
    df['go_id'].astype(str)
    df['go_label'].astype(str)
    df['evidence_type'].astype(str)
    df['protein_class'].astype(str)

    print(df.loc[df['symbol'] == 'NOD2'])
    print(len(df))

    '''
       write dataframe to csv
    '''
    df.to_csv(Config.GENE_ANNOTATION_FILES['output_gene_info'])


def merge_tissue_expression_location():

    gtex_df = pd.read_csv(Config.GENE_TISSUE_EXPRESSION['gtex'], sep='\t')
    # EntrezID	ENSEMBL_ID	Symbol	EFO	Label (OTv8_or_earlier)	Tissue	Max Fold Change
    gtex_df = gtex_df.rename(columns={'EntrezID': 'entrez_id',
                                      'ENSEMBL_ID': 'ensembl_gene_id',
                                      'Symbol': 'symbol',
                                      'EFO': 'disease_id',
                                      'Label (OTv8_or_earlier)': 'disease_label',
                                      'Max Fold Change': 'max_fold_change'})
    gtex_df['entrez_id'].astype(str)
    gtex_df['ensembl_gene_id'].astype(str)
    gtex_df['symbol'].astype(str)
    newdf = gtex_df.assign(source="GTExv6", tissue_label=gtex_df['Tissue'].apply(lambda x: x.split('_')[0]))
    newdf.tissue_label.str.replace("_GTExv6", "")
    newdf = newdf.drop('Tissue', 1)
    cols = newdf.columns.tolist()
    cols = cols[:5] + ['tissue_label', 'source'] + ['max_fold_change']
    print(cols)
    df = newdf[cols]
    print(df.loc[df['symbol'] == 'NOD2'])
    df.to_csv(Config.GENE_TISSUE_EXPRESSION['output_tissue_expression'])


def calculate_expression_levels():

    df = pd.read_csv(Config.GENE_TISSUE_EXPRESSION['output_tissue_expression'], index_col=0)
    print(len(df))
    formula = lambda x: "%.2f"%(1 - (1 /math.sqrt(x/ 5)))
    df = df.assign(expression_score=df['max_fold_change'].apply(formula))
    print(len(df))
    df.to_csv(Config.GENE_TISSUE_EXPRESSION['output_tissue_expression_withscore'])

    # drop the disease label
    df = df.drop('disease_label', 1)

    # merge the evidence with the expression
    # select the distinct diseases from the file and get the relevant tissues
    for key, filename in Config.VERSION1_SCORE_FILES.iteritems():

        print("Reading original %s"%filename)
        dt_df = pd.read_csv(filename, index_col=0)

        '''
        tissue_label,source,max_fold_change,expression_score
        new_column = []
        idx =
        dt_df.insert(idx, 'tissue_label', value)
        '''
        print(len(dt_df))
        #dt_df['tissue_label'] = np.nan
        # pd.DataFrame(np.zeros((len(dt_df), 1)))
        #dt_df['max_fold_change'] = np.zeros((len(dt_df), 1))
        #dt_df['expression_score'] = np.zeros((len(dt_df), 1))


        merged_df = pd.merge(dt_df, df, how='left', on=['entrez_id', 'ensembl_gene_id', 'disease_id', 'symbol'])
        cond1 = merged_df['expression_score'] >= 0
        #print(merged_df[cond1])
        print(len(merged_df), len(merged_df[cond1]))
        merged_df['max_fold_change'].fillna(0, inplace=True)
        merged_df['expression_score'].fillna(0, inplace=True)
        merged_df['tissue_label'].fillna('Unspecified', inplace=True)
        merged_df['source'].fillna('Unspecified', inplace=True)
        print(merged_df)
        print(merged_df[cond1])

        merged_df.to_csv(Config.VERSION2_SCORE_FILES[key])

def merge_QTQ():

    # read gene info again
    df = pd.read_csv(Config.GENE_ANNOTATION_FILES['output_gene_info'], index_col=0)
    print(df)
    qtq_df = pd.read_csv(Config.GENE_ANNOTATION_FILES['qtq'])
    # ENSEMBL_ID,TargetClass,Topology_Type,Target_Location,ExAC_LoF,% human query gene identical to target Mouse gene,GTEX_median_all_tissues
    qtq_df = qtq_df.rename(columns={
                                      'ENSEMBL_ID': 'ensembl_gene_id',
        'TargetClass': 'target_class',
        'Topology_Type': 'topology_type',
        'Target_Location': 'target_location',
        '% human query gene identical to target Mouse gene': 'pc_mouse_gene_identity',
    })

    # rename
    # select the column we need
    qtq_filtered= qtq_df[['ensembl_gene_id', 'target_class', 'topology_type', 'target_location', 'ExAC_LoF', 'pc_mouse_gene_identity', 'GTEX_median_all_tissues', 'description' ]]
    df = pd.merge(df, qtq_filtered, how='left', on=['ensembl_gene_id'])
    df.to_csv(Config.GENE_ANNOTATION_FILES['output_gene_info_qtq'])


def clean_disease_location():
    '''
    Read disease location and simplify
    '''
    df = pd.read_csv(Config.GENE_TISSUE_EXPRESSION['disease_location'], sep='\t')
    df = df.assign(disease_id=df['disease_iri'].apply(lambda x: x.split('/')[-1]), disease_location_id=df['disease_location_iri'].apply(lambda x: x.split('/')[-1]))
    df = df[['disease_id', 'disease_location_id', 'disease_location_label']]
    print(df[:10])
    df.to_csv(Config.GENE_TISSUE_EXPRESSION['output_disease_location'])

def parse_scoring_matrices():

    hgnc_df = pd.read_csv(Config.GENE_ANNOTATION_FILES['hgnc_mappings'], sep='\t')
    hgnc_df['entrez_id'].astype(str)
    hgnc_df['uniprot_id'].astype(str)
    entrez_df = hgnc_df[['ensembl_gene_id', 'entrez_id']]


    df = pd.read_csv(Config.DRAFT_SCORE_FILE_URLS['datasource_scores'])
    '''
    rename columns
    EnsemblId	Symbol	OntologyId	Label	Is direct	overall	expression_atlas	uniprot	gwas_catalog	phewas_catalog	eva	uniprot_literature	genomics_england	gene2phenotype	reactome	slapenrich	phenodigm	cancer_gene_census	eva_somatic	uniprot_somatic	intogen	chembl	europepmc
    '''
    df = df.rename(columns={
                            'EnsemblId': 'ensembl_gene_id',
                            'Symbol': 'symbol',
                            'OntologyId': 'disease_id',
                            'Label': 'disease_label',
                            'Is direct': 'direct_association',
                            'overall': 'overall_score'})

    df = pd.merge(df, entrez_df, how='left', on=['ensembl_gene_id'])
    cols = df.columns.tolist()
    print(cols)
    cols = cols[-1:] + cols[0:-1]
    print(cols)
    df = df[cols]
    hgnc_df['entrez_id'].astype(str)
    df.to_csv(Config.DRAFT_SCORE_FILE_URLS['output_datasource_scores'])
    # remove drug info from ChEMBL and overall score
    df = df.drop('chembl', 1)
    df = df.drop('overall_score', 1)
    df.to_csv(Config.DRAFT_SCORE_FILE_URLS['output_datasource_scores_nodrugs'])

    df = pd.read_csv(Config.DRAFT_SCORE_FILE_URLS['datatype_scores'])
    cols = df.columns.tolist()
    print(cols)

    '''
    "EnsemblId","Symbol","OntologyId","Label","Is direct","overall","genetic_association","somatic_mutation","known_drug","rna_expression","affected_pathway","animal_model","literature"
    '''
    df = df.rename(columns={
        'EnsemblId': 'ensembl_gene_id',
        'Symbol': 'symbol',
        'OntologyId': 'disease_id',
        'Label': 'disease_label',
        'Is direct': 'direct_association',
        'overall': 'overall_score'})

    df = pd.merge(df, entrez_df, how='left', on=['ensembl_gene_id'])
    cols = df.columns.tolist()
    print(cols)
    cols = cols[-1:] + cols[0:-1]
    print(cols)
    df = df[cols]
    hgnc_df['entrez_id'].astype(str)
    df.to_csv(Config.DRAFT_SCORE_FILE_URLS['output_datatype_scores'])
    df = df.drop('known_drug', 1)
    df = df.drop('overall_score', 1)
    df.to_csv(Config.DRAFT_SCORE_FILE_URLS['output_datatype_scores_nodrugs'])

def parse_pharmaprojects():
    df = pd.read_csv(Config.PHARMAPROJECTS['original_file'])
    df = df.drop('Target_Indication', 1)
    df = df.rename(columns={
        'Ensembl_ID': 'ensembl_gene_id',
        'EntrezGeneID': 'entrez_id',
        'EFO_ID': 'disease_id'})
    print(df[:10])
    df.to_csv(Config.PHARMAPROJECTS['output_pharmaprojects'])


def merge_expression_to_associations():

    exp_df = pd.read_csv(Config.GENE_TISSUE_EXPRESSION['output_tissue_expression'])

    for k, filename in Config.VERSION1_SCORE_FILES.iteritems():
        print(filename)
        output = filename.replace('gene_disease', 'gene_expression_disease')
        df = pd.read_csv(filename)
        df = pd.merge(df, exp_df, how='left', on=['entrez_id','ensembl_gene_id','disease_id'])
        print(df)
        return

def generate_short_excel_version():

    # combine Evidence from OpenTargets_PharmaProjects in single file
    pp_df = pd.read_csv(Config.PHARMAPROJECTS['output_pharmaprojects'], index_col=0)

    ot_dt_df = pd.read_csv(Config.VERSION2_SCORE_FILES['output_datatype_scores'], index_col=0)
    df = pd.merge(pp_df, ot_dt_df, how='inner', on=['entrez_id', 'ensembl_gene_id', 'disease_id'])
    df.to_csv(Config.PHARMAPROJECTS['output_opentargets_pharmaprojects'])


def main():

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    #merge_gene_annotations()
    #merge_tissue_expression_location()
    #clean_disease_location()
    #parse_scoring_matrices()
    #parse_pharmaprojects()
    #merge_expression_to_associations()
    #calculate_expression_levels()
    #merge_QTQ()
    #parse_pharmaprojects()
    generate_short_excel_version()
    


if __name__ == "__main__":
    main()