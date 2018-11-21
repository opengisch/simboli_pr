# To be launched from the python console of QGIS2

import os
from qgis.core import (
    QgsStyleV2, QgsSymbolLayerV2Utils, QgsRenderContext, QgsMarkerSymbolV2,
    QgsLineSymbolV2, QgsFillSymbolV2)
from qgis.PyQt.QtCore import QSize


class SymbologyImages(object):

    def save_pngs_from_list_file(self, list_file, output_directory):
        with open(list_file) as f:
            for i, symbol_name in enumerate(f.readlines()):
                symbol_name = symbol_name.strip()
                symbol = self.get_symbol(symbol_name)

                pixmap = self.create_pixmap_from_symbol(
                    symbol,
                    self.calculate_scale_factor(symbol, symbol_name)
                )
                self.save_pixmap_into_png(
                    pixmap,
                    os.path.join(
                        output_directory,
                        symbol_name + ".png"
                    )
                )

    def get_symbol(self, symbol_name):
        """Return the QgsSymbolV2 or None if not found"""

        style = QgsStyleV2().defaultStyle()
        return style.symbol(symbol_name)

    def create_pixmap_from_symbol(self, symbol, factor):
        context = QgsRenderContext()
        context.setScaleFactor(factor)

        pixmap = QgsSymbolLayerV2Utils.symbolPreviewPixmap(
            symbol, QSize(142, 71), context)
        return pixmap

    def save_pixmap_into_png(self, pixmap, file_name):
        image = pixmap.toImage()
        image.setDotsPerMeterX(23622)
        image.setDotsPerMeterY(23622)
        image.save(file_name, "PNG")

    def calculate_scale_factor(self, symbol, symbol_name):
        factor = 10
        if isinstance(symbol, QgsMarkerSymbolV2):
            factor = (12 / symbol.size()) * 4.6
        elif isinstance(symbol, QgsLineSymbolV2):
            factor = 30
        elif isinstance(symbol, QgsFillSymbolV2):
            factor = 10

        # Special cases
        special_cases = {
            'P_26_124_0004': 7,
            'P_26_125_0008': 15,
            'P_26_125_0009': 15,
            'P_26_125_0009': 15,
            'P_26_125_0010': 15,
            'P_26_125_0011': 15,
            'P_26_125_0012': 15,
            'P_26_125_0013': 15,
            'P_26_125_0014': 15,
            'P_26_125_0015': 15,
            'P_26_125_0016': 15,
            'P_26_125_0017': 15,
            'P_27_127_0007': 9,
            'P_31_159_0002': 20,
            'P_33_167_0002': 10,
            'L_19_005_0004': 10,
            'L_19_005_0009': 20,
            'L_19_006_0005': 20,
            'L_19_006_0013': 20,
            'L_19_102_0006': 7,
            'L_20_099_0001': 10,
            'L_20_099_0002': 10,
            'L_20_099_0003': 10,
            'L_20_099_0004': 10,
            'L_20_099_0005': 10,
            'L_20_099_0006': 10,
            'L_20_099_0007': 10,
            'L_20_099_0008': 10,
            'L_20_099_0009': 10,
            'L_20_099_0010': 10,
            'L_20_099_0011': 10,
            'L_20_099_0013': 10,
            'L_20_099_0014': 10,
            'L_20_099_0015': 10,
            'L_20_100_0001': 10,
            'L_21_105_0010': 10,
            'L_21_107_0001': 5,
            'L_21_107_0002': 5,
            'L_21_107_0003': 10,
            'L_21_107_0004': 5,
            'L_21_107_0005': 7,
            'L_21_107_0006': 10,
            'L_21_107_0007': 5,
            'L_21_107_0008': 5,
            'L_21_107_0009': 10,
            'L_21_107_0010': 7,
            'L_21_108_0001': 5,
            'L_21_110_0001': 5,
            'L_21_110_0002': 10,
            'L_21_110_0003': 10,
            'L_21_110_0004': 5,
            'L_21_169_0001': 7,
            'L_22_092_0001': 20,
            'L_22_092_0002': 20,
            'L_22_092_0003': 20,
            'L_22_092_0004': 7,
            'L_22_092_0005': 10,
            'L_22_092_0006': 7,
            'L_22_092_0007': 10,
            'L_22_092_0008': 7,
            'L_22_092_0009': 7,
            'L_22_092_0010': 7,
            'L_22_092_0011': 7,
            'L_22_092_0012': 10,
            'L_22_092_0013': 8,
            'L_22_093_0011': 10,
            'L_22_093_0017': 20,
            'L_22_093_0033': 20,
            'L_22_093_0034': 20,
            'L_22_095_0001': 10,
            'L_22_096_0003': 20,
            'L_22_097_0001': 10,
            'L_22_163_0001': 15,
            'L_22_163_0002': 7,
            'L_22_163_0003': 15,
            'L_25_116_0002': 20,
            'S_01_138_0002': 5,
            'S_10_041_0004': 5,
        }

        if symbol_name in special_cases:
            return special_cases[symbol_name]

        return factor


if __name__ in ['__main__', '__console__']:
    symbology_images = SymbologyImages()
    symbology_images.save_pngs_from_list_file(
        '/home/mario/workspace/repos/symbology-ti/ti-utils/fase2.txt',
        '/home/mario/workspace/repos/symbology-ti/result/png')
