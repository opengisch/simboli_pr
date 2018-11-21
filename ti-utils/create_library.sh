#!/usr/bin/env bash

set -e

# Remove old svg because they are not overwritten
rm ../result/libreria/svg/*

# Create library.xml and svg files with patch applied
python library.py

# Remove svg path from library.xml
sed -i -- 's/\/home\/mario\/workspace\/repos\/symbology-ti\/result\/libreria\/svg\///g' ../result/libreria/libreria.xml

# Fix very thin lines
sed -i -- 's/v="0.0352778"/v="0"/g' ../result/libreria/libreria.xml

# Remove emf files
rm ../result/libreria/svg/*.emf
