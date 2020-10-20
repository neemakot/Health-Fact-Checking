# Explainable Fact-Checking for Public Health Claims

This repository contains data and code for the paper [Explainable Fact-Checking for Public Health Claims](https://neemakot.github.io/publication/emnlp2020/) which will be presented at [The 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP 2020)](https://2020.emnlp.org/papers/main).

## Introduction

Fact-checking is the task of verifying the veracity of claims by assessing their assertions against credible evidence. The vast majority of fact-checking studies focus exclusively on political claims. Very little research explores fact-checking for other topics, specifically subject matters for which expertise is required. We present the first study of explainable fact-checking for claims which require specific expertise. For our case study we choose the setting of public health. To support this case study we construct a new dataset PUBHEALTH of 11.8K claims accompanied by journalist crafted, gold standard explanations (i.e., judgments) to support the fact-check labels for claims. We explore two tasks: veracity prediction and explanation generation. We also define and evaluate, with humans and computationally, three coherence properties of explanation quality. Our results indicate that, by training on in-domain data, gains can be made in explainable, automated fact-checking for claims which require specific expertise.

## Dataset

We present PUBHEALTH, a dataset for two fact-checking tasks: claim verification and generating natural language explanations for verified claims. The dataset can be found under ``data/PUBHEALTH/``. 

The following is an example of an instance of the PUBHEALTH dataset:

|  Field              |  Example        |
| ------------   | ------- |
| __claim__  	     | Expired boxes of cake and pancake mix are dangerously toxic. |
| __explanation__    | What's True:  Pancake and cake mixes that contain mold can cause life-threatening allergic reactions. What's False: Pancake and cake mixes that have passed their expiration dates are not inherently dangerous to ordinarily healthy people, and the yeast in packaged baking products does not "over time develops spores." |
| __label__          |  mixture      |
| __claim URL__     | https://www.snopes.com/fact-check/expired-cake-mix/ |
| __author(s)__        | David Mikkelson | 
| __date published__ | April 19, 2006 |
| __tags__           | Food, allergies, baking, cake |


Further information about the dataset can be found in the ``DATASHEET`` and ``README`` provided under `data/`.


## Reference

If you use the dataset, please cite it as formatted below.

```
@inproceedings{kotonya-toni-2020-explainable,
  title = "Explainable Automated Fact-Checking for Public Health Claims",
  author = "Kotonya, Neema  and Toni, Francesca",
  booktitle = "2020 Conference on Empirical Methods in Natural Language Processing",
  publisher = "Association for Computational Linguistics",
  address = "Online",
  month = nov,
  year = "2020"
}
```

## Contact

Please feel free to contact [Neema Kotonya](mailto:nk2418@ic.ac.uk) if you have any queries.