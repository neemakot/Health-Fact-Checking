# PUBHEALTH DATASET

Here is a brief outline of the PUBHEALTH dataset presented in this repository.

## Explainable Fact-Checking for Public Health Claims

Description of the tab-separated format in which the data is presented:

### train.tsv and dev.tsv:

Column 1: claim ID							
Column 2: claim text 
Column 3: date published
Column 4: explanation
Column 5: fact checkers / news report authors
Column 6: main_text
Column 7: evidence sources for the claim
Column 8: label 
Column 9: tags related to the claim (named subjects)
Column 10: claim URL	
Column 11: website 


### test.tsv:

Column 1: claim ID							
Column 2: claim text 
Column 3: date published
Column 4: fact checkers / news report authors
Column 5: main_text
Column 6: evidence sources for the claim
Column 7: tags related to the claim (named subjects)
Column 8: claim URL	
Column 9: website

### lexicon.txt:

Lexicon of 6,952 public health words and phrases. 


Note: this dataset (and the lexicon used to build it) is a revised/curated version of that which is mentioned in the EMNLP 2020 paper to include 381 additional health-related claims in order to assist with ongoing COVID-19 fact checking efforts. Some instances have been omitted from the dataset either due to limited relevance, because the claim was poorly defined or due to multiple instances of near identical claims in the dataset. The methodology employed to acquire these new dataset instances is the same as that which is mentioned in the EMNLP paper.


For queries please contact [Neema Kotonya](nk2418@ic.ac.uk).

v1.0 19 October 2020