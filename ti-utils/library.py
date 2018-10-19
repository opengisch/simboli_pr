
import os
import sys
sys.settrace
sys.path.append('../slyr')

from qgis.PyQt.QtWidgets import QApplication

from slyr.parser.symbol_parser import read_symbol
from slyr.parser.initalize_registry import initialize_registry

import argparse
from io import BytesIO
from qgis.core import QgsStyle, QgsUnitTypes
from slyr.bintools.extractor import Extractor
from slyr.parser.symbol_parser import read_symbol, UnreadableSymbolException
from slyr.converters.qgis import Symbol_to_QgsSymbol, Context

from slyr.parser.initalize_registry import initialize_registry

initialize_registry()

path = "/home/mario/workspace/repos/symbology-ti/bin"
destination = "/home/mario/workspace/repos/symbology-ti/ti-utils/output/libreria.xml"

blobs = []

style = QgsStyle()

context = Context()

context.units = QgsUnitTypes.RenderMillimeters
context.relative_paths = True
context.picture_folder = 'output'
context.convert_fonts = True
context.force_svg_instead_of_raster = True
context.parameterise_svg = False
context.embed_pictures = False

a = QApplication([])

for fn in os.listdir(path):
    file = os.path.join(path, fn)
    if os.path.isfile(file):
        blobs.append(file)
        symbol_name = os.path.splitext(fn)[0]
#        print(symbol_name)

        with open(file, 'rb') as f:
            context.symbol_name = symbol_name
            symbol = read_symbol(f, debug=False)
            qgis_symbol = Symbol_to_QgsSymbol(symbol, context)
            style.addSymbol(symbol_name, qgis_symbol)

style.exportXml(destination)
