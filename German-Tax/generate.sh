#!/bin/sh -x

#./extractMetadata.py $1 > ./meta/${1%.xml}-meta.yml
./convertXml2Java.py $1 int
