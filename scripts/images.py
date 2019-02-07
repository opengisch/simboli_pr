import os
from qgis.core import (
    QgsStyle, QgsSymbolLayerUtils, QgsRenderContext, QgsMarkerSymbol,
    QgsLineSymbol, QgsFillSymbol)
from qgis.PyQt.QtCore import QSize, QSettings
from qgis.testing import start_app


class Images():
    """This class generates png images of symbols using the QGIS API."""

    def __init__(self, list_file, output_directory):
        """
        Constructor

        :param list_file: the path of a file containing the list of symbols
        for which generate the images.
        :param output_directory: the path of the directory where the images
        will be stored.
        """
        self.list_file = list_file
        self.output_directory = output_directory
        start_app()

    def run(self):
        """
        Start the images generation
        """

        main_dir_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), os.pardir)

        s = QSettings()
        svg_paths = []
        svg_paths.append(os.path.join(main_dir_path, 'result/libreria/svg/'))
        s.setValue('svg/searchPathsForSVG', svg_paths)

        style = QgsStyle.defaultStyle()
        style.importXml(os.path.join(
            main_dir_path, 'result/libreria/libreria.xml'))

        with open(self.list_file) as f:
            for i, symbol_name in enumerate(f.readlines()):

                symbol_name = symbol_name.strip()
                symbol = self._get_symbol(symbol_name)

                pixmap = self._create_pixmap_from_symbol(
                    symbol,
                    *self._calculate_scale_factor_padding(symbol, symbol_name)
                )

                self._save_pixmap_into_png(
                    pixmap,
                    os.path.join(
                        self.output_directory,
                        symbol_name + ".png"
                    )
                )

    def _get_symbol(self, symbol_name):
        """Return the QgsSymbol or None if not found"""

        style = QgsStyle().defaultStyle()
        return style.symbol(symbol_name)

    def _create_pixmap_from_symbol(self, symbol, scale_factor, padding):
        context = QgsRenderContext()
        context.setScaleFactor(scale_factor)

        pixmap = QgsSymbolLayerUtils.symbolPreviewPixmap(
            symbol, QSize(142, 71), padding, context)
        return pixmap

    def _save_pixmap_into_png(self, pixmap, file_name):
        image = pixmap.toImage()
        image.setDotsPerMeterX(23622)
        image.setDotsPerMeterY(23622)
        image.save(file_name, "PNG")

    def _calculate_scale_factor_padding(self, symbol, symbol_name):
        factor = 10
        padding = 0
        if isinstance(symbol, QgsMarkerSymbol):
            factor = (12 / symbol.size()) * 4.6
        elif isinstance(symbol, QgsLineSymbol):
            factor = 7
            padding = 0
        elif isinstance(symbol, QgsFillSymbol):
            factor = 10

        # Special cases
        # Symbol_code: (scale_factor, padding)
        special_cases = {
            'P_26_124_0004': (7, 0),
            'P_26_125_0008': (15, 0),
            'P_26_125_0009': (15, 0),
            'P_26_125_0009': (15, 0),
            'P_26_125_0010': (15, 0),
            'P_26_125_0011': (15, 0),
            'P_26_125_0012': (15, 0),
            'P_26_125_0013': (15, 0),
            'P_26_125_0014': (15, 0),
            'P_26_125_0015': (15, 0),
            'P_26_125_0016': (15, 0),
            'P_26_125_0017': (15, 0),
            'P_27_127_0007': (9, 0),
            'P_31_159_0002': (20, 0),
            'P_33_167_0002': (10, 0),
            'L_19_101_0001': (7, 5),
            'L_19_101_0002': (7, 5),
            'L_19_101_0003': (7, 5),
            'L_19_101_0005': (7, 8),
            'L_21_110_0001': (4, 15),
            'L_21_110_0004': (5, 10),
            'L_22_096_0003': (7, 8),
            'L_22_097_0001': (5, 12),
            'L_22_163_0001': (7, 13),
            'S_01_138_0002': (5, 0),
            'S_10_041_0004': (5, 0)
        }

        if symbol_name in special_cases:
            return special_cases[symbol_name]

        return (factor, padding)


if __name__ == '__main__':

    main_dir_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.pardir)

    images = Images(
        os.path.join(main_dir_path, 'scripts/fase2.txt'),
        os.path.join(main_dir_path, 'result/png'))
    images.run()
