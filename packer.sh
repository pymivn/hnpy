#!/bin/bash

rm pymiHNslack.zip
zip -r pymiHNslack.zip *.py hnpy
HERE=$(pwd)
DIR=$(mktemp -d --tmpdir=$HERE)
cd $DIR; pip install -r ../requirements.txt -t .
zip -r $HERE/pymiHNslack.zip *
mv $DIR /tmp
