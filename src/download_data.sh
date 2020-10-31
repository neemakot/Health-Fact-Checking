#!/bin/bash

URL='https://drive.google.com/uc?export=download&id=1eTtRs5cUlBP5dXsx-FTAlmXuB6JQi2qj'
PATH_TO_DATA='../data/'
FILENAME='../data/PUBHEALTH.zip'

wget --no-check-certificate $URL -P $PATH_TO_DATA -O $FILENAME

unzip -d $PATH_TO_DATA $FILENAME 
