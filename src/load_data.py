"""preprocess_data.py.
   Created on 25 April 2020.
"""

import random
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from operator import itemgetter
import pandas as pd
import numpy as np
import os
import nltk
import tensorflow as tf

from tensorflow.python.client import device_lib
device_lib.list_local_devices()

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"

config =  tf.compat.v1.ConfigProto(log_device_placement=True)
sess = tf.compat.v1.Session(config=config)


# def format_data_summarization(corpus):
#     data = pd.DataFrame(columns=['input', 'label', 'explanation'])

#     for instance in corpus.iterrows():
#         label = instance['label']
#         model_input = ''.join(
#             ['[CLS]{}[SEP]'.format(sent) for sent in sent_tokenize(
#                 instance['text'])
#             ])
#         data = data.append([model_input, label, instance['explanation']])

#     data.to_csv('../../data/processed_data.csv')


def format_data_as_stories(path_to_data):
    corpus = pd.read_csv(path_to_data)

    for index, row in corpus.iterrows():
        main_text_sentences = [sent.strip() + '\n\n' 
                               for sent in 
                               sent_tokenize(row['story'])]

        explanation_sentences = ['@highlight' + '\n\n' + sent.strip() + '\n\n' 
                                 for sent in 
                                 sent_tokenize(row['summary'])]

        with open('../../../langmodels/summarization/{0:05d}.story'.format(index), 'w+') as fp:
            fp.writelines(main_text_sentences)
            fp.writelines(explanation_sentences)

def format_data_as_mappings(train, val, test):
    with open('../../data/summarization/mapping_train', 'w') as fp:
        fp.writelines([url + '\n' for url in train])
    with open('../../data/summarization/mapping_test', 'w') as fp:
        fp.writelines([url + '\n' for url in test])
    with open('../../data/summarization/mapping_valid', 'w') as fp:
        fp.writelines([url + '\n' for url in val])



def select_evidence_sentences(path_to_corpus, k):
    """Select top k evidence sentences based on sentence transformer model."""
    corpus = pd.read_csv(path_to_corpus)
    sentence_transformer_model = SentenceTransformer('bert-base-nli-mean-tokens')
    corpus['top_k'] = np.empty([len(corpus),], dtype=str)

    for index, row in corpus.iterrows():
        claim = row['claim']
        sentences = [claim] + [
                     sentence for sentence in sent_tokenize(row['main_text'])]

        sentence_embeddings = sentence_transformer_model.encode(sentences)
        claim_embedding = sentence_embeddings[0]
        sentence_embeddings = sentence_embeddings[1:]
        cosine_similarity_emb = {}

        for sentence, embedding in zip(sentences, sentence_embeddings):
            cosine_similarity_emb[sentence] = np.linalg.norm(cosine_similarity(
                [claim_embedding, embedding]))

        top_k = dict(sorted(cosine_similarity_emb.items(), 
                            key=itemgetter(1))[:k]) 
        corpus.at[index, 'top_k'] = ' '.join(key for key in top_k.keys())

    df = pd.DataFrame(columns=['claim', 'top_k', 'label', 'explanation'])
    df['claim'] = corpus['claim']
    df['top_k'] = corpus['top_k']
    df['label'] = corpus['label']
    df['explanation'] = corpus['explanation']
    df.to_csv('../../data/formatted_data.csv')


if __name__ == '__main__':
    with tf.device('/gpu:1'):
        PATH_TO_CORPUS = '../../data/PUBHEALTH/data.csv'
        select_evidence_sentences(PATH_TO_CORPUS, k=5)




