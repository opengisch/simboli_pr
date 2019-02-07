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
                    self._calculate_scale_factor(symbol, symbol_name)
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

    def _create_pixmap_from_symbol(self, symbol, factor):
        context = QgsRenderContext()
        context.setScaleFactor(factor)

        pixmap = QgsSymbolLayerUtils.symbolPreviewPixmap(
            symbol, QSize(142, 71), 0, context)
        return pixmap

    def _save_pixmap_into_png(self, pixmap, file_name):
        image = pixmap.toImage()
        image.setDotsPerMeterX(23622)
        image.setDotsPerMeterY(23622)
        image.save(file_name, "PNG")

    def _calculate_scale_factor(self, symbol, symbol_name):
        factor = 10
        if isinstance(symbol, QgsMarkerSymbol):
            factor = (12 / symbol.size()) * 4.6
        elif isinstance(symbol, QgsLineSymbol):
            factor = 30
        elif isinstance(symbol, QgsFillSymbol):
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

    main_dir_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.pardir)

    images = Images(
        os.path.join(main_dir_path, 'scripts/fase2.txt'),
        os.path.join(main_dir_path, 'result/png'))
    images.run()
