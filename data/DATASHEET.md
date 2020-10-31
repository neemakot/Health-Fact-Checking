# Datasheet for the PUBHEALTH dataset for explainable fake news detection of public health claims.

Author: [Neema Kotonya](https://neemakot.github.io/)

Organization: Department of Computing, Imperial College London

Dataset: [PUBHEALTH](https://drive.google.com/file/d/1eTtRs5cUlBP5dXsx-FTAlmXuB6JQi2qj/view)

The template for this document is taken from the paper [Datasheets for Datasets (Gebru et al., 2019)](https://www.microsoft.com/en-us/research/uploads/prod/2019/01/1803.09010.pdf).


## Motivation for Dataset Creation


* __For what purpose was the dataset created?__  (e.g., were there specific
tasks in mind, or a specific gap that needed to be filled?)

The dataset was created to explore fact-checking of difficult to verify claims i.e., those which require 
expertise from outside of the journalistics domain, in this case biomedical and public health expertise.

It was also created in response to the lack of fact-checking datasets which provide gold standard natural language 
explanations for verdicts/labels.

* __What (other) tasks could the dataset be used for?__ Are
there obvious tasks for which it should _not_ be used?

Other fact-checking tasks e.g., assessment of claim checkworthiness.

* __Has the dataset been used for any tasks already?__ If so,
where are the results so others can compare (e.g., links to
published papers)?

The dataset was used for two automated fact-checking tasks: veracity prediction and generating explanations as summaries in Explainable Automated Fact-Checking for Public Health Claims (Kotonya and Toni, 2020).

* __Who funded the creation of the dataset?__ If there is an
associated grant, provide the grant number.

There was no grant or funding provided for the creation of this dataset. 

## Dataset Composition

* __What are the instances?__ (that is, examples; e.g., documents, images, people, countries) Are there multiple types
of instances? (e.g., movies, users, ratings; people, interactions between them; nodes, edges)

Each instance is a fact-check, news review report or news article.

* __Are relationships between instances made explicit in the data?__ 

There are no relationships between instances in the dataset.


* __What data does each instance consist of? “Raw” data (e.g., unprocessed text or images)?__ Features/attributes? Is there a label/target associated with instances? If the instances are related to people, are subpopulations identified (e.g., by age, gender, etc.) and what is their distribution?

The dataset consists entirely of text, the following are the fields present in the dataset.

| Field    |
| ---------|
| claim ID | 
| claim    |  
| claim URL|
| main_text|
| veracity label|
| explanation for veracity label|
| subject tags |
| data published |
| fact checkers / authors |
| URLs for evidence sources |


* __Is everything included or does the data rely on external resources?__ (e.g., websites, tweets, datasets) If external
resources, a) are there guarantees that they will exist, and remain constant, over time; b) is there an official archival version. Are there licenses, fees or rights associated with any of the data?

Only URLs are provided for evidence sources. We will soon provide full evidence documents for dataset instances.

* __Are there recommended data splits or evaluation measures?__ (e.g., training, development, testing; accuracy/AUC)

The data provided is already split into ``train.tsv``, ``dev.tsv``, and ``test.tsv``.

* __What experiments were initially run on this dataset?__ Have a summary of those results and, if available, provide
the link to a paper with more information here.

The experiments which have been run this dataset and their results can be found in the EMNLP paper.

## Data Collection Process

* __How was the data collected?__ (e.g., hardware apparatus/sensor, manual human curation, software program, software interface/API; how were these constructs/measures/methods validated?)

The dataset was retrieved from the following fact-checking, news reviews and news websites: 

| URL  				        | Type |
| ----------------------------------| -------------|
| http://snopes.com/		 		| fact-checking|
| http://politifact.com/     		| fact-checking|
| http://truthorfiction.com/ 		| fact-checking|
| https://www.factcheck.org/ 		| fact-checking |
| https://fullfact.org/				| fact-checking |
| https://apnews.com/ 				| news   |
| https://uk.reuters.com/           | news   |
| https://www.healthnewsreview.org/ | health news review |

* __Who was involved in the data collection process?__ (e.g., students, crowdworkers) How were they compensated? (e.g.,
how much were crowdworkers paid?)

The data collection process was automated through scripts.

* __Over what time-frame was the data collected?__ Does the collection time-frame match the creation time-frame?

The data was collected in May 2020. We have since expanded the dataset in October 2020 in order to help with ongoing COVID-19 fact-checking efforts.

* __How was the data associated with each instance acquired?__ Was the data directly observable (e.g., raw text,
movie ratings), reported by subjects (e.g., survey responses), or indirectly inferred/derived from other data (e.g., part of speech tags; model-based guesses for age or language)? If the latter two, were they validated/verified and if so how?

The data was directly observable. 

* __Does the dataset contain all possible instances?__ Or is
it, for instance, a sample (not necessarily random) from a
larger set of instances?

Yes, this is a sample of instances from a larger fact-checking dataset which was collected. The instances in this dataset are related to public health claims, however those from the larger dataset were related to a wide variety of subject matter.


* __Is there information missing from the dataset and why?__ (this does not include intentionally dropped instances; it
might include, e.g., redacted text, withheld documents) Is this data missing because it was unavailable?

Some data is missing fields are missing from instances in the dataset because they were unavailable.

* __Are there any known errors, sources of noise, or redundancies in the data?__

Not as far as we know.


## Data Preprocessing

* __What preprocessing/cleaning was done?__ (e.g., discretization or bucketing, tokenization, part-of-speech tagging,
SIFT feature extraction, removal of instances, processing of missing values, etc.)

The preprocessing of the data is outlined in the EMNLP paper.

* __Was the “raw” data saved in addition to the preprocessed/cleaned data?__ (e.g., to support unanticipated future uses)

The "raw" data has been saved.

* __Is the preprocessing software available?__ 

Yes, we are making the preprocessing scripts available under ``src/clean_data.py``.

* __Does this dataset collection/processing procedure achieve the motivation for creating the dataset stated
in the first section of this datasheet?__

Yes, it does.


## Dataset Maintenance

* __Who is supporting/hosting/maintaining the dataset?__ How does one contact the owner/curator/manager of the
dataset (e.g. email address, or other contact info)?

Please email [Neema Kotonya](mailto:nk2418@ic.ac.uk).


* __Will the dataset be updated? How often and by whom?__ How will updates/revisions be documented and communicated (e.g., mailing list, GitHub)? Is there an erratum?

Yes, we hope to update the data periodically. New updates and revisions will be documented and communicated on GitHub.

* __If the dataset becomes obsolete how will this be communicated?__

We will communicate this through the GitHub repo.

* __Is there a repository to link to any/all papers/systems that use this dataset?__

No there is not, but we will create one in the future if needed.

* __If others want to extend/augment/build on this dataset, is there a mechanism for them to do so?__ If so, is there
a process for tracking/assessing the quality of those contributions. What is the process for communicating/distributing
these contributions to users?

Not yet, however we will create this when the need arises.


## Legal & Ethical Considerations

* __Does the dataset contain information that might be considered sensitive or confidential? (e.g., personally identifying information)__

Not to our knowledge, but if it is brought to our attention that we are mistaken we will make the appropriate corrections to the dataset.

* __Does the dataset contain information that might be considered inappropriate or offensive?__

Not to our knowledge, but if it is brought to our attention that we are mistaken we will make the appropriate corrections to the dataset.




