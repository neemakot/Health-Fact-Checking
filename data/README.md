# PUBHEALTH DATASET

Here is a brief overview of the PUBHEALTH dataset presented in this GitHub repository.

You can [click here](https://drive.google.com/file/d/1eTtRs5cUlBP5dXsx-FTAlmXuB6JQi2qj/view) to download the data or use the following command

```
 cd ../src
 ./download_data.sh
```

## Explainable Fact-Checking for Public Health Claims

Train/dev/test data splits:

|           |\# Instances|
| --------- | -----------|
| train.tsv |	9,817    | 
| dev.tsv   |   1,227    |
| test.tsv  |  1,235     |
| total     |  12,279	 |

Description of the tab-separated format in which the data is presented:

* train.tsv and dev.tsv:

| Columns        |  
| -------------- |
| claim ID       | 
| claim          |  
| date published |
| explanation    |
| fact checkers / authors |
| main evidence text |
| evidence sources for the claim |
| label |
| tags related to the claim (named subjects) |
| URLs for evidence sources |
| claim URL |
| website name |


* test.tsv:

| Columns        |  
| -------------- |
| claim ID       | 
| claim          |  
| date published |
| fact checkers / authors |
| main evidence text |
| evidence sources for the claim |
| tags related to the claim (named subjects) |
| URLs for evidence sources |
| claim URL |
| website name |

* lexicon.txt:

Lexicon of 6,952 public health words and phrases. 


Note: This dataset, and the lexicon used to construction it, are revised/curated versions of those which are mentioned in the EMNLP 2020 paper to include 447 additional health-related claims in order to assist with ongoing COVID-19 fact checking efforts. Some instances have been omitted from the dataset either due to limited relevance, because the claim was poorly defined or due to multiple instances of near identical claims in the dataset. The methodology employed to acquire these new dataset instances is the same as that which is mentioned in the EMNLP paper.


For queries please contact [Neema Kotonya](nk2418@ic.ac.uk).

v1.0 19 October 2020