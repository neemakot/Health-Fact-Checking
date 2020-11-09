#!/bin/bash

URL='https://drive.google.com/uc?export=download&id=1qDjbniulHhSI73JoZHs3eWdVPQBMH2Gt'
PATH_TO_DATA='../data/'
FILENAME='../data/PUBHEALTH_EVIDENCE_DOCS.zip'

wget --no-check-certificate $URL -P $PATH_TO_DATA -O $FILENAME

mkdir $PATH_TO_DATA

unzip -d $PATH_TO_DATA $FILENAME

rm -rf '../data/__MACOSX/' 

rm -rf '../data/PUBHEALTH_EVIDENCE_DOCS.zip' 