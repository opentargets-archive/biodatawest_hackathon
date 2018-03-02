# biodatawest_hackathon
Python and R Code and documentation for the BioData West 2018 hackathon

### Files

```
https://console.cloud.google.com/storage/browser/biodata-west-hackathon/version1/?project=open-targets
```
 * Disease location (EFO to Uberon): disease_uberon_location.csv
 	- disease_id: disease identifier
 	- disease_location_id: UBERON location identifier
 	- disease_location_label: UBERON location corresponding name
 * GTEx gene expression and disease relevance: gene_disease_gtex_tissue_expression.csv
 	- entrez_id: Entrez gene identifier
	- ensembl_gene_id: ENSEMBL gene identifier
	- symbol: gene symbol
	- disease_id: disease identifier
	- disease_label: disease name
	- tissue_label: tissue name as described in GTEx
	- source: GTEx version 6
	- max_fold_change: gene expression fold change (if mRNA expression in the indicated tissue for this gene is at least 5-fold above the median tissue and within 5-fold of the highest expression tissue)
 * Gene symbol, Entrez Gene ID, Ensembl Gene ID, UniProt Protein ID, GO Annotations, Protein Class: gene_info.csv
 
 * PharmaProjects gene indication pairs: Pprojects_drugs.csv
 	- Note this data is interpreted from Pharmaprojects XML output (as of 5Aug2017) and cannot be kept in any form beyond the period of this workshop. Errors in interpretation may have occurred.
	- Target_Indication: merge of Ensembl|EFO IDs 
	- Ensembl ID: target identifier (ENSEMBL)
	- EFO_ID: disease identifier (EFO)
	- EntrezGeneID: target identifier (EntrezGene)
	- MeSH_ID: disease identifier (Medical Subject Heading)
	- Disease Type: Neoplasm (cancer) or Non-Neoplasm
	- Clinical Label_PP (Succeeded; Clinical Failure; In Progress Clinical): Indicates the best reported outcome for any asset for this target-indication pair. 
	- Furthest Phase: Indicates the furthest reported phase for any asset for this target-indication pair. This includes assets reported as In Progress Clinical.
	- Therapeutic Direction (Activator; Inhibitor; Mixed/Unknown): Indicates the collective nature of the assets if >90% are in the same direction.
	- Indication with First Clinical Outcome of Target (Y;N): Indicates whether the indication was the first one with a reported clinical outcome for the indicated target.
	- Types of Assets (Selective; Non-Selective): Indicated whether the assets are reported by Pharamaprojects to be against a single target or multiple targets.
	- Suggested Dataset Utility (Training; Test; Neither):  For those TIP pairs reported as First Clinical Outcomes, we have chosen ~80% of these as "Training" and 20% as "Test", doing our best to balance the indications attempted by each.  Note that outcome data is very highly correlated (similar diseases are subsequently attempted with assets against a successfully treated disease), and so typical cross-validation schemes are not useful.
	
 * Gene disease associations per datatype (with and without drugs): gene_disease_associations_datatype.csv, gene_disease_associations_datatype_nodrugs.csv
 * Gene disease associations per datasource (with and without ChEMBL scores):  gene_disease_associations_datasource_with_expression.csv
 
| Column name         | Description |
| --------------------|-------------|
| entrez_id           | Entrez gene identifier |
| ensembl_gene_id     | Ensembl gene identifier |
| symbol              | gene symbol |
| disease_id          | disease identifier |
| disease_label       | disease name |
| direct_association  | Is the association drawn from a direct evidence or propagated based on the disease classification? |
| overall_score       | overall score of the association (aggregate the others) |
| expression_atlas    | Expression Atlas association score
| uniprot             | UniProt genetic score |
| gwas_catalog        | GWAS Catalog genetic score |
| phewas_catalog      | PheWAS Catalog genetic score |
| eva| EVA (ClinVar) genetic score |
| uniprot_literature| UniProt literature curated genetic score |
| genomics_england| Genomics England PanelApp genetic score |
| gene2phenotype| Gene2Phenotype genetic score |
| reactome| Reactome affected pathways score |
| slapenrich| SlapEnrich cancer affected pathways score |
| phenodigm| Phenodigm (Animal model) score |
| cancer_gene_census| Cancer Gene Census score |
| eva_somatic| EVA (ClinVar) somatic mutations score |
| uniprot_somatic| UniProt somatic mutations score |
| intogen| InToGEN cancer driver gene score |
| chembl| ChEMBL clinical trial score |
| europepmc| EuroPMC literature score |
| tissue_label| Relevant tissue name when known |
| source| GTEx v6 |
| max_fold_change| gene expression fold change (if mRNA expression in the indicated tissue for this gene is at least 5-fold above the median tissue and within 5-fold of the highest expression tissue) |
| expression_score | normalised gene expression score for max_fold_change | 
