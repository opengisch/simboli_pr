#!/usr/bin/env bash

set -e

# Remove old result
rm -rf ../result

# Create result directory structure
mkdir ../result
mkdir ../result/libreria
mkdir ../result/libreria/svg
mkdir ../result/png
mkdir ../result/qgis_project

# Create library.xml and svg files with patch applied
python3 library.py

# Remove svg path from libreria.xml
sed -i -- 's/\/shared\/result\/libreria\/svg\///g' ../result/libreria/libreria.xml

# Fix very thin lines
sed -i -- 's/v="0.0352778"/v="0"/g' ../result/libreria/libreria.xml

# Remove emf files
rm -f ../result/libreria/svg/*.emf

# Create qgs project and gpkg demo data
python3 project.py

# Create png images
python3 images.py

# Create a zip file with the result
zip -r ../result/libreria.zip ../result/
