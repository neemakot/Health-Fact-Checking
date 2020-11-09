"""extract_evidence.py.
   Created on 24 April 2020.
"""

import os
import re
import io
import requests
import string
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader, utils
import bleach

import nltk
nltk.download('punkt')

from nltk import tokenize
from collections import defaultdict
from sklearn.utils import shuffle


def create_dataset():
    """Create dataset from news articles and fact-checks."""
    full_data = pd.read_csv(
        '../data/medical_event_claims/full_data_for_med 2.csv')
    full_data['label'] = full_data['label'].str.lower().str.strip()


    for index, item in full_data.iterrows():
        if full_data.at[index, 'website'] == 'politifact':
            if full_data.at[index, 'claim'].startswith('Says'):
                if full_data.at[index, 'speaker'] in ['Facebook posts', 'Bloggers']:
                    full_data.at[index, 'claim'] = full_data.at[index, 'speaker'][:-1] + ' ' + full_data.at[index, 'claim']
                else:    
                    full_data.at[index, 'claim'] = full_data.at[index, 'speaker'] + ' ' + full_data.at[index, 'claim']

    full_data = full_data.drop(columns=['title', 'original_claim_quote',
                                        'author', 'occupation', 'speaker',
                                        'Unnamed: 0'], axis=1)


    news_data = pd.read_csv('../data/data_cleaned.csv', low_memory=False)

    news_data = news_data[news_data['subjects'].str.lower().str.contains(
                                    'health|medical|environment|medicine|science|drugs')]
    # news_data = news_data[news_data['subjects'].str.lower().str.contains(
    #                                 'health')]
    news_data['label'] = ['true'] * len(news_data)
    news_data['website'] = [None] * len(news_data)
    news_data = news_data.drop(columns=['id'], axis=1)
    print(len(news_data))


    healthnews_data = pd.read_csv('../data/healthnewsreview.csv')
    # healthnews_data = healthnews_data[ ~healthnews_data['claim'].str.contains('Ray ID:') &
    #                   ~healthnews_data['claim'].str.contains('404') &
    #                   ~healthnews_data['claim'].str.contains('Error') ]
    healthnews_data = healthnews_data.drop_duplicates(subset='claim', keep='first')
    healthnews_data = healthnews_data.drop(columns=['Unnamed: 0'], axis=1)
    healthnews_data['main_text'] = healthnews_data['main_text'].replace('\n', ' ')
    print('health news review: {}'.format(len(healthnews_data)))

    for index, item in news_data.iterrows():
        if 'reuters.com' in item['url']:
            news_data.at[index, 'website'] = 'reuters'
        else:
            news_data.at[index, 'website'] = 'apnews'
            news_data.at[index, 'subjects'] = news_data.at[
                index, 'subjects'].replace('\n', ', ').replace('\'', '')

        if not item['claim'].endswith('.'):
            news_data.at[index, 'claim'] = item['claim'] + '.'
            # print(news_data.at[index, 'claim'])

    for prefix in ['AP FACT CHECK:', 'Correction:', 'AP EXCLUSIVE:',
                   'AP Interview:', 'How ',]:
        news_data = news_data[~news_data['claim'].astype(str).str.startswith(
                              prefix)]

    # print(healthnews_data[healthnews_data.claim.str.contains('CWRU researchers find')].date_published)
    news_data['standardised'] = news_data['label']
    full_data['standardised'] = full_data['label']
    full_data = pd.concat([news_data, healthnews_data, full_data], sort=True)
    # print(full_data[full_data.claim.str.contains('CWRU researchers find')].date_published)
    # Also clean text rows
    for index, item in full_data.iterrows():
        full_data.at[index, 'explanation'] = ' '.join([
            sent.strip().replace('\n', ' ').replace('•','') for sent 
            in sent_tokenize(str(item['explanation']))]
            )

        full_data.at[index, 'main_text'] = ' '.join([
            sent.strip().replace('\n', ' ').replace('Pants on Fire', '') for sent 
            in sent_tokenize(str(item['main_text']))
            if ('RELATED:' not in sent and 
                'RELATED STORY:' not in sent and
                'RELATED COVERAGE:' not in sent and 
                'RELATED FACT-CHECK:' not in sent
               )]
            )
    # print(full_data[full_data.claim.str.contains('CWRU researchers find')].date_published)
    # Standardize dates - so that they are all September 25, 2019
    months = {'Jan': 'January', 'Feb': 'February', 'Mar': 'March',
              'Apr': 'April', 'May': 'May', 'Jun': 'June', 'Jul': 'July',
              'Aug': 'August', 'Sep': 'September', 'Oct': 'October', 
              'Nov': 'November', 'Dec': 'December' 
              }
    
    full_data = full_data[full_data['claim'].notnull()]
    # for index, item in full_data.iterrows():
    #     try:
    #         full_data.at[index, 'claim'] = str(full_data.at[index, 'claim'])
    #     except:
    #         pass

    for index, item in full_data.iterrows():
        if 'healthnewsreview' in str(full_data.at[index, 'website']):
            continue

        date = str(item['date_published'])
        if date == 'nan' or date == np.nan:
            full_data.at[index, 'date_published'] = ''
            continue

        if item['website'] == 'truthorfiction':
            # e.g. September 25, 2019
            full_data.at[index, 'date_published'] = date.strip()

        if item['website'] == 'apnews':
            # e.g. September 25, 2019
            full_data.at[index, 'date_published'] = date.strip()
 
        if item['website'] == 'politifact':
            # e.g. September 25 2019
            parts = date.split(' ')
            full_data.at[index, 'date_published'] = ' '.join(
            [parts[0], parts[1]+',', parts[2]])

        if item['website'] == 'fullfact':
            # e.g. 25th Sep 2019
            parts = date.split(' ')
            day = parts[0]
            month = months[parts[1]]
            year = parts[2]
            full_data.at[index, 'date_published'] = ' '.join(
                [month, day[:-2]+',', parts[2]])

        if item['website'] == 'snopes':
            # e.g. 25 September 2019
            parts = date.split(' ')
            full_data.at[index, 'date_published'] = ' '.join(
                [parts[1], parts[0]+',', parts[2]])

    date_format = re.compile(
        '[A-Za-z]+ ([1-9]|[1-2][0-9]|3([01])), (199[0-9]|(20((0|1)[0-9]|20)))')

    # full_data['date_published'] = full_data['date_published'].str.strip()
    print('truthorfiction: {}'.format(len(full_data[full_data.website == 'truthorfiction'])))
    print(full_data[full_data.claim.str.contains('CWRU researchers find')].date_published)

    not_included = full_data[~(
        (full_data['date_published'].str.match(date_format))|
                           (full_data['date_published'] == '')
                            ) ]
    # print(not_included['date_published'])

    full_data = full_data[(full_data['date_published'].str.match(date_format))|
                           (full_data['date_published'] == '')
                            ]


    full_data.to_csv('../data/medical_event_claims/unprocessed.csv')
    print(len(full_data[(full_data['website']== 'reuters') | (full_data['website']== 'apnews')]))
    print(len(full_data))
    print('truthorfiction: {}'.format(len(full_data[full_data.website == 'truthorfiction'])))


# Standardise to 4 labels- Unknown/Unproven, True, False, Mixture
def standardise_labels(full_data):
    """Standardise labels."""

    # Retrieve and apply standardised labels.
    labels = pd.read_csv('../data/misc/labels_standardized.csv')
    labels = labels.drop_duplicates('original', keep='first')
    labels_map = dict(zip(labels['original'], labels['standardised']))

    # p = list(set([label for label in full_data['label'] if label not in labels['original']]))

    full_data['standardised'] = [labels_map[old_label] for old_label in full_data['label']]

    # Match labels with remaining claims that don't have standardised label.
    claims_and_labels = pd.read_csv('../data/misc/claims_label.csv')
    claim_label_map = dict(zip(claims_and_labels['claim'],
                               claims_and_labels['label']))

    for index, row in full_data.iterrows():
        full_data.at[index, 'claim'] = full_data.at[index, 'claim'].strip('"')
        if row['claim'] in claim_label_map:
            full_data.at[index, 'standardised'] = claim_label_map[
                                                        row['claim']].strip()

    no_label = full_data[full_data.standardised.isnull()]
    print(len(no_label))
    for claim in no_label['claim']:
        print(claim)

    # Remove claims for which standardised labels can't be found.
    not_standardised = full_data[full_data['standardised'].isnull()]

    full_data['standardised'] = full_data['standardised'].replace({'fiction': 'false'})

    print(full_data['standardised'].value_counts())
    print(len(full_data))
    return full_data


def count_unique(passage: str, keywords: list) -> int:
    count = 0
    passage = passage.translate(str.maketrans('', '', string.punctuation))
    words = []
    for keyword in keywords:
        if keyword in passage:
            count += 1
            words.append(keyword)
    # print(count)
    if count > 3:
        pass
        # print(words)
    return count


def filter_medical_claims(full_data):
    """Filter the claims which are related to medical fact-checking."""

    # remove nan explanations from data 
    full_data = full_data[(full_data['explanation'].notnull()) &
                           (full_data['explanation'].str.len() > 3) ]

    with open('../data/misc/vocabulary/abbreviations.txt') as fp:
        abbrv = [word.strip() for word in fp.readlines()]

    with open('../data/misc/terms.txt') as fp:
        words = [word.lower().strip().replace('(', '\(').replace(')', '\)') for word in fp.readlines()] 
        # append(word.lower().strip().replace('(', '').replace(')', ''))

    # Words added manually, these words were not scraped from health websites
    # used to create terms.txt.

    print(len(list(set(words+abbrv))))

    keywords = list(set(words))
    abbrv = list(set(abbrv))

    with open('../data/lexicon.txt', 'w') as fp:
        fp.writelines(sorted([k + '\n' for k in keywords]))
        fp.writelines(sorted([a + '\n' for a in abbrv]))

    full_data['count_'] = full_data['main_text'].map(lambda x: count_unique(x.lower(), keywords)
                             ) + full_data['main_text'].map(lambda x: count_unique(x, abbrv))
    full_data['count_claim'] = full_data['claim'].map(lambda x: count_unique(x.lower(), keywords)
                                ) + full_data['claim'].map(lambda x: count_unique(x, abbrv))

    # full_data['countn_'] = full_data['main_text'].str.lower().str.count('|'.join(list(set(keywords)))
    #     ) + full_data['main_text'].str.lower().str.count('|'.join(list(set(abbrv))))
    # full_data['countm_claim'] = full_data['claim'].str.lower().str.count('|'.join(list(set(keywords)))
    #     ) + full_data['claim'].str.lower().str.count('|'.join(list(set(abbrv))))

    # full_data['countn_'].to_csv('../data/countx.csv')
    # full_data['countm_claim'].to_csv('../data/countx_claim.csv')

    full_data = full_data[
        (full_data['count_'] > 3) |
        (full_data['count_claim'] > 3) |
        (full_data['website'].str.contains('healthnewsreview')) |
        # (full_data['subjects'].str.contains('health')) |
        # (full_data['subjects'].str.contains('medical')) |
        # (full_data['subjects'].str.contains('medicine')) |
        # (full_data['subjects'].str.contains('nutrition')) 
        ]

    print('1 number healthnewsreview: {}'.format(len(full_data[full_data['website'] == 'healthnewsreview'])))

    # Drop explanations that are too short
    # print(len(full_data[(full_data['claim'].str.len() > 25) & (full_data['website'] == 'healthnewsreview')]))
    # print(len(full_data[(full_data['claim'].str.len() < 500) & (full_data['website'] == 'healthnewsreview')]))

    full_data = full_data[(full_data['claim'].str.len() > 25)]
    full_data = full_data[(full_data['claim'].str.len() < 500)]

    # ----TODO ---: Clean explanation data, split and get rid of everything after the first 
    # 'Share the Facts'
    for index, row in full_data.iterrows():
        if 'Share the Facts' in full_data.at[index, 'explanation']:
            full_data.at[index, 'explanation'], _ = full_data.at[index, 'explanation'].split('Share the Facts', 1)
        if '.sharethefacts' in full_data.at[index, 'explanation']:
            full_data.at[index, 'explanation'], _ = full_data.at[index, 'explanation'].split('.sharethefacts', 1)


    print('2 After explanation filter number healthnewsreview: {}'.format(len(full_data[full_data['website'] == 'healthnewsreview'])))

    full_data = full_data[(full_data['explanation'].str.len() >= 40)] 
    full_data = full_data[(full_data['main_text'].str.len() >= 400)] 
    full_data = full_data[~(full_data['claim'].str.endswith('?'))]
    # full_data = full_data[~(full_data['explanation'].str.endswith('?'))]
    full_data = full_data[~((full_data['standardised'].isnull()))]

    
    full_data = full_data[(full_data['standardised'] == 'true') |
                          (full_data['standardised'] == 'false') |
                          (full_data['standardised'] == 'mixture') |
                          (full_data['standardised'] == 'unproven')
                          ]
    # print(len(full_data[(full_data['standardised'].isnull()) & (full_data['website'] == 'healthnewsreview')]))
    print('3 After explanation filter number healthnewsreview: {}'.format(len(full_data[full_data['website'] == 'healthnewsreview'])))

    full_data = shuffle(full_data)
    # full_data = full_data.sample(frac=1, axis=1).reset_index(drop=True)

    full_data.index.name = 'claim_id'

    print(np.mean(full_data['count_']))
    # full_data['count_'].to_csv('../data/count_.csv')
    full_data = full_data.drop(columns=['count_', 'Unnamed: 0', 'count_claim', 'label',
                                ], axis=1)

    full_data = full_data.rename(columns={"standardised": "label"})

    full_data['claim'] = full_data['claim'].astype(str)
    full_data['date_published'] = full_data['date_published'].astype(str)
    full_data['date_published'] = full_data['date_published'].replace({'nan': ''})

    full_data = full_data.fillna(' ')

    # Save PUBHEALTH claims
    full_data.to_csv('../data/PUBHEALTH/data.csv')

    test_size = int(len(full_data)*0.1)
    print(test_size)

    train = full_data[:test_size*8]
    dev = full_data[test_size*8:test_size*9]
    test = full_data[test_size*9:]


    train.to_csv('../../Health-Fact-Checking/data/PUBHEALTH/train.tsv', sep='\t',)
    dev.to_csv('../../Health-Fact-Checking/data/PUBHEALTH/dev.tsv', sep='\t',)

    # test = test.drop(columns=['label', 'explanation'], axis=1)
    test.to_csv('../../Health-Fact-Checking/data/PUBHEALTH/test.tsv', sep='\t')

    print('TRAIN')
    print(train['label'].value_counts())

    print('DEV')
    print(dev['label'].value_counts())

    # full_data[test_size:test_size*2].to_csv('../../Health-Fact-Checking/data/PUBHEALTH/dev.tsv', sep='\t')
    # full_data[test_size*2:]
    # test.to_csv('../../Health-Fact-Checking/data/PUBHEALTH/train.tsv', sep='\t',)

    # print(sorted(list(full_data['date_published']))[-1])
    # print(sorted(list(full_data['date_published']))[0])    

    print(full_data['label'].value_counts())
    print(len(full_data))
    print(full_data['website'].value_counts())


if __name__ == '__main__':
    pd.set_option('display.max_columns', None) 
    pd.set_option('display.max_colwidth', -1)
