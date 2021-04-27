# Explainable Fact-Checking for Public Health Claims

This repository contains data and code for the paper [Explainable Fact-Checking for Public Health Claims (Kotonya and Toni, 2020)](https://arxiv.org/abs/2010.09926). This research will be presented at The 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP 2020).




## Introduction

Fact-checking is the task of verifying claims (i.e., distinguishing between false stories and facts) by assessing the  assertions made by claims against credible evidence. The vast majority of fact-checking studies focus exclusively on political claims. Very little research explores fact-checking for other topics, specifically subject matters for which _expertise_ is required. We present the first study in [explainable fact-checking](https://neemakot.github.io/project/survey/) for claims which require specific expertise. 

For our case study we choose the setting of public health. To support this, we construct a new dataset __PUBHEALTH__ of 11.8K claims accompanied by journalist-crafted, gold standard explanations (i.e., judgments) to support the fact-check labels for claims. We explore two tasks: veracity prediction and explanation generation. We also define and evaluate, with humans and computationally, three coherence properties of explanation quality. Our results indicate that, by training on in-domain data, gains can be made in explainable, automated fact-checking for claims which require specific expertise.


## Data

### PUBHEALTH fact-checking dataset

We present __PUBHEALTH__, a comprehensive dataset for explainable automated fact-checking of public health claims. Each instance in the __PUBHEALTH__ dataset has an associated veracity label (true, false, unproven, mixture). Furthermore each instance in the dataset has an _explanation_ text field. The explanation is a justification for which the claim has been assigned a particular veracity label. 

The dataset can be [downloaded here](https://drive.google.com/file/d/1eTtRs5cUlBP5dXsx-FTAlmXuB6JQi2qj/view). 

OR

The dataset can be acquired using the following commands

```
 cd src
 ./download_data.sh
```

The following is an example instance of the __PUBHEALTH__ dataset:

|  Field              |  Example                                                     |
| -----------------   | -------------------------------------------------------------|
| __claim__  	      | Expired boxes of cake and pancake mix are dangerously toxic. |
| __explanation__     | What's True:  Pancake and cake mixes that contain mold can cause life-threatening allergic reactions. What's False: Pancake and cake mixes that have passed their expiration dates are not inherently dangerous to ordinarily healthy people, and the yeast in packaged baking products does not "over time develops spores." |
| __label__           |  mixture                                                     |
| __claim URL__       | https://www.snopes.com/fact-check/expired-cake-mix/          |
| __author(s)__       | David Mikkelson                                              | 
| __date published__  | April 19, 2006                                               |
| __tags__            | food, allergies, baking, cake                                |
| __main_text__        |   In April 2006, the experience of a 14-year-old who had eaten pancakes made from a mix that had gone moldy was described in the popular newspaper column Dear Abby. The account has since been circulated widely on the Internet as scores of concerned homemakers ponder the safety of the pancake and other baking mixes lurking in their larders [...]       |
| __evidence sources__    | [1] Bennett, Allan and Kim Collins.  “An Unusual Case of Anaphylaxis: Mold in Pancake Mix.” American Journal of Forensic Medicine & Pathology.   September 2001   (pp. 292-295). [2] Phillips, Jeanne.   “Dear Abby.” 14 April 2006   [syndicated column]. |

More information about the __PUBHEALTH__ dataset can be found in [DATASHEET.md](data/DATASHEET.md) and [README.md](data/README.md) provided under under ``data/``, including test/train/dev splits, and data collection and processing information.


### PUBHEALTH evidence documents

We have are also collecting the original evidence documents cited in the fact-checking articles. We are currently updating this collection, however the current version can be downloaded using the following commands

```
 cd src
 ./download_evidence_docs.sh
```

Alternatively, you can download the evidence documents [here](https://drive.google.com/file/d/1qDjbniulHhSI73JoZHs3eWdVPQBMH2Gt/view?usp=sharing).

The evidence documents are all text files with names formatted as ```doc_<CLAIM_ID>_<EVIDENCE_NUMBER>.txt```.


## Requirements

This project is built using Py36 and Tensorflow. To install the dependencies use the following command

```
pip install -r requirements.txt
```

There is the full list of requirements including versions:

* [Python 3.6](https://www.python.org/downloads/release/python-360/)

_Machine Learning, NLP, evaluation and visualization packages_:
* [bert](https://pypi.org/project/bert/)==2.2.0
* [bleach](https://pypi.org/project/bleach/)==3.0.2
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)==4.8.2
* [Keras](https://pypi.org/project/Keras/)==2.3.1
* [matplotlib](https://pypi.org/project/matplotlib/)==3.0.1
* [numpy](https://pypi.org/project/numpy/)==1.18.1
* [py-rouge](https://pypi.org/project/py-rouge)==1.1
* [PyYAML](https://pypi.org/project/PyYAML/)==5.3.1
* [PyPDF2](https://pypi.org/project/PyPDF2/)==1.26.0
* [requests](https://pypi.org/project/requests/)==2.13.0
* [scikit-learn](https://pypi.org/project/scikitlearn/)==0.1.1
* [sentence-transformers](https://pypi.org/project/sentence-transformers/)==0.3.8
* [tensorflow](https://pypi.org/project/tensorflow/)==1.15.0
* [tokenizers](https://pypi.org/project/tokenizers/)==0.7.0
* [tqdm](https://pypi.org/project/tqdm/)==4.43.0


## Reference

If you use the dataset, please cite the paper as formatted below.

```
@inproceedings{kotonya-toni-2020-explainable,
    title = "Explainable Automated Fact-Checking for Public Health Claims",
    author = "Kotonya, Neema  and
      Toni, Francesca",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.623",
    pages = "7740--7754",
}
```

## Contact

Please feel free to contact [Neema Kotonya](mailto:nk2418@ic.ac.uk) if you have any queries.
