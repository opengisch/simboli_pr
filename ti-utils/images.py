# To be launched from the python console of QGIS2

import os
from qgis.core import (
    QgsStyleV2, QgsSymbolLayerV2Utils, QgsRenderContext)
from qgis.PyQt.QtCore import QSize


class SymbologyImages(object):

    def save_pngs_from_list_file(self, list_file, output_directory):
        with open(list_file) as f:
            for i, symbol_name in enumerate(f.readlines()):
                symbol = self.get_symbol(symbol_name)
                pixmap = self.create_pixmap_from_symbol(symbol)
                self.save_pixmap_into_png(
                    pixmap,
                    os.path.join(
                        output_directory,
                        symbol_name.strip() + ".png"
                    )
                )

    def get_symbol(self, symbol_name):
        """Return the QgsSymbolV2 or None if not found"""

        style = QgsStyleV2().defaultStyle()
        return style.symbol(symbol_name.strip())

    def create_pixmap_from_symbol(self, symbol):
        context = QgsRenderContext()
        context.setScaleFactor(5)

        pixmap = QgsSymbolLayerV2Utils.symbolPreviewPixmap(
            symbol, QSize(142, 71), context)
        return pixmap

    def save_pixmap_into_png(self, pixmap, file_name):
        image = pixmap.toImage()
        image.setDotsPerMeterX(23622)
        image.setDotsPerMeterY(23622)
        image.save(file_name, "PNG")


if __name__ in ['__main__', '__console__']:
    symbology_images = SymbologyImages()
    symbology_images.save_pngs_from_list_file(
        '/home/mario/workspace/repos/symbology-ti/ti-utils/fase2.txt',
        '/home/mario/workspace/tmp/simboli_cantone_20181120/out_tmp')
