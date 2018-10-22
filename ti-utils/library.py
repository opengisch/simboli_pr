import os
import sys
from shutil import copyfile
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsStyle, QgsUnitTypes

sys.path.append('../slyr')

from slyr.parser.symbol_parser import read_symbol
from slyr.parser.initalize_registry import initialize_registry
from slyr.parser.symbol_parser import read_symbol, UnreadableSymbolException
from slyr.converters.qgis import Symbol_to_QgsSymbol, Context
from slyr.parser.initalize_registry import initialize_registry

initialize_registry()

path = "/home/mario/workspace/repos/symbology-ti/bin"
destination = ("/home/mario/workspace/repos/symbology-ti/"
               "ti-utils/output/libreria/libreria.xml")

patched_xml_path = ("/home/mario/workspace/repos/symbology-ti/"
                    "ti-utils/xml_patch")

patched_svg_path = ("/home/mario/workspace/repos/symbology-ti/"
                    "ti-utils/svg_patch")

# Symbols for whitch it exists a manually modified xml
patched_xml = ['S_01_081_0017', 'S_01_081_0018',
               'S_14_145_0015', 'S_05_019_0001',
               'L_19_006_0008', 'L_25_116_0001',
               'S_11_042_0013']

# Symbols for whitch it exists a manually modified svg
patched_svg = ['P_26_120_0015', 'P_33_172_0001',
               'P_26_122_0007', 'P_26_124_0004_1']

blobs = []

style = QgsStyle()

context = Context()

context.units = QgsUnitTypes.RenderMillimeters
context.relative_paths = True
context.picture_folder = 'output/libreria'
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

        if symbol_name in patched_xml:
            xml_file = os.path.join(
                patched_xml_path,
                symbol_name + '.xml')
            style.importXml(xml_file)
            print(f"Patch symbol {symbol_name} with {xml_file}")
            continue

        with open(file, 'rb') as f:
            context.symbol_name = symbol_name
            symbol = read_symbol(f, debug=False)
            qgis_symbol = Symbol_to_QgsSymbol(symbol, context)

            style.addSymbol(symbol_name, qgis_symbol)

style.exportXml(destination)

for svg in patched_svg:
    svg_src = os.path.join(patched_svg_path, svg + '.svg')
    svg_dest = os.path.join("/home/mario/workspace/repos/symbology-ti/ti-utils/output/libreria", svg + '.svg')
    
    copyfile(svg_src, svg_dest)
    print(f"Patch svg {svg_dest} with {svg_src}")
    
