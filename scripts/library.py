import os
import sys
from shutil import copyfile
from qgis.core import QgsStyle, QgsUnitTypes
from qgis.PyQt.QtWidgets import QApplication

main_dir_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir)

sys.path.append(os.path.join(main_dir_path, 'slyr'))

from slyr.parser.symbol_parser import read_symbol
from slyr.parser.initalize_registry import initialize_registry
from slyr.parser.symbol_parser import read_symbol, UnreadableSymbolException
from slyr.converters.qgis import Symbol_to_QgsSymbol, Context
from slyr.parser.initalize_registry import initialize_registry


class Library():
    """This class generates the xml symbol library and the svg images
    contained in the symbols"""

    def __init__(self, bin_directory, output_directory, patched_xml_directory,
                 patched_svg_directory):
        """
        Constructor

        :param bin_directory: the path of the directory where the bin files
        of the symbols are stored.
        :param output_directory: the path of the directory where the library
        and the svg directory will be stored.
        :param patched_xml_directory: the path of the directory with patches
        for the library.
        :param patched_svg_directory: the path of the directory with patches
        for svg images.
        """
        self.bin_directory = bin_directory
        self.output_directory = output_directory
        self.patched_xml_directory = patched_xml_directory
        self.patched_svg_directory = patched_svg_directory
        initialize_registry()

    def run(self):
        """
        Start the library generation
        """

        patched_xml = ['S_01_081_0017', 'S_01_081_0018',
                       'S_14_145_0015', 'S_05_019_0001',
                       'L_19_006_0008', 'L_25_116_0001',
                       'S_11_042_0013', 'L_21_105_0002',
                       'L_21_107_0010', 'L_22_092_0003',
                       'L_22_092_0008', 'L_22_092_0009',
                       'L_22_092_0010', 'L_22_092_0011',
                       'L_22_092_0012', 'P_31_159_0002',
                       'S_01_081_0010', 'S_01_089_0016',
                       'S_05_017_0008', 'S_10_041_0004',
                       'S_13_046_0012', 'S_13_046_0018',
                       'S_14_048_0008', 'S_18_071_0001',
                       'P_28_157_0001', 'P_32_160_0001',
                       'P_33_161_0001']

        # Symbols for which it exists a manually modified svg
        patched_svg = ['P_26_120_0015', 'P_33_172_0001',
                       'P_26_122_0007', 'P_26_124_0004_1',
                       'L_20_099_0006', 'L_20_099_0007',
                       'L_20_099_0009', 'L_20_099_0011',
                       'P_28_157_0001', 'P_32_160_0001',
                       'P_33_161_0001']

        blobs = []
        style = QgsStyle()
        context = Context()
        context.units = QgsUnitTypes.RenderMillimeters
        context.relative_paths = True
        context.picture_folder = os.path.join(
            self.output_directory, 'svg')
        context.convert_fonts = True
        context.force_svg_instead_of_raster = True
        context.parameterise_svg = False
        context.embed_pictures = False

        a = QApplication([])

        for fn in os.listdir(self.bin_directory):
            file = os.path.join(self.bin_directory, fn)
            if os.path.isfile(file):
                blobs.append(file)
                symbol_name = os.path.splitext(fn)[0]

                with open(file, 'rb') as f:
                    context.symbol_name = symbol_name
                    symbol = read_symbol(f, debug=False)
                    qgis_symbol = Symbol_to_QgsSymbol(symbol, context)

                    if symbol_name in patched_xml:
                        xml_file = os.path.join(
                            self.patched_xml_directory,
                            symbol_name + '.xml')
                        style.importXml(xml_file)
                        print("Patch symbol {} with {}".format(
                            symbol_name, xml_file))
                        continue

                    style.addSymbol(symbol_name, qgis_symbol)

        style.exportXml(
            os.path.join(self.output_directory, 'libreria.xml'))

        for svg in patched_svg:
            svg_src = os.path.join(self.patched_svg_directory, svg + '.svg')
            svg_dest = os.path.join(
                self.output_directory, 'svg', svg + '.svg')

            copyfile(svg_src, svg_dest)
            print("Patch svg {} with {}".format(svg_dest, svg_src))


if __name__ == '__main__':

    main_dir_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.pardir)

    library = Library(
        os.path.join(main_dir_path, 'bin'),
        os.path.join(main_dir_path, 'result/libreria'),
        os.path.join(main_dir_path, 'scripts/xml_patch'),
        os.path.join(main_dir_path, 'scripts/svg_patch'))
    library.run()
