#!/bin/bash
# cleanup mongo and solr
python src/debates.py solr-admin --delete
python src/debates.py mongo-admin --delete
# load to mongo and solr
python src/debates.py s3-to-mongo-solr HRC_20220929T1000 --debug
python src/debates.py s3-to-mongo-solr HRC_20220328T1000 --debug
python src/debates.py s3-to-mongo-solr HRC_20221010T1000 --debug
