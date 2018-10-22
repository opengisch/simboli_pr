# To be run into QGIS2 python console

from qgis.core import (
    QgsStyleV2, QgsMapLayerRegistry, QgsVectorLayer, QgsFeature,
    QgsGeometry, QgsPoint, QgsCategorizedSymbolRendererV2,
    QgsRendererCategoryV2, QgsSymbolLayerV2Utils, QgsRenderContext)

from qgis.PyQt.QtCore import QSize


class SymbologyProject(object):

    def __init__(self):
        self.layer_points = None
        self.layer_lines = None
        self.layer_polygons = None

    def create_layers(self):

        self.layer_points = QgsVectorLayer(
            'Point?crs=epsg:2056&field=id:string(13)', 'points', "memory")
        self.layer_points.setRendererV2(QgsCategorizedSymbolRendererV2('id'))

        self.layer_lines = QgsVectorLayer(
            'LineString?crs=epsg:2056&field=id:string(13)', 'lines', "memory")
        self.layer_lines.setRendererV2(QgsCategorizedSymbolRendererV2('id'))

        self.layer_polygons = QgsVectorLayer(
            'Polygon?crs=epsg:2056&field=id:string(13)', 'polygons', "memory")
        self.layer_polygons.setRendererV2(QgsCategorizedSymbolRendererV2('id'))

        QgsMapLayerRegistry.instance().addMapLayers(
            [self.layer_points, self.layer_lines, self.layer_polygons])

    def get_layers(self):
        self.layer_points = QgsMapLayerRegistry.instance().mapLayersByName(
            'points')[0]
        self.layer_points.setRendererV2(QgsCategorizedSymbolRendererV2('id'))
        self.layer_lines = QgsMapLayerRegistry.instance().mapLayersByName(
            'lines')[0]
        self.layer_lines.setRendererV2(QgsCategorizedSymbolRendererV2('id'))
        self.layer_polygons = QgsMapLayerRegistry.instance().mapLayersByName(
            'polygons')[0]
        self.layer_polygons.setRendererV2(QgsCategorizedSymbolRendererV2('id'))

    def draw_feature_with_symbol(self, pos_x, pos_y, symbol_name):
        if symbol_name.startswith('P_'):
            layer = self.layer_points
            geometry = QgsGeometry.fromPoint(QgsPoint(pos_x, pos_y))
        elif symbol_name.startswith('L_'):
            layer = self.layer_lines
            points = []
            points.append(QgsPoint(pos_x, pos_y))
            points.append(QgsPoint(pos_x + 200, pos_y))
            geometry = QgsGeometry.fromPolyline(points)
        elif symbol_name.startswith('S_'):
            layer = self.layer_polygons
            points = []
            points.append(QgsPoint(pos_x, pos_y))
            points.append(QgsPoint(pos_x + 200, pos_y))
            points.append(QgsPoint(pos_x + 200, pos_y + 10))
            points.append(QgsPoint(pos_x, pos_y + 10))
            points.append(QgsPoint(pos_x, pos_y))
            geometry = QgsGeometry.fromPolygon([points])

        data_provider = layer.dataProvider()
        feature = QgsFeature()
        feature.setFields(layer.fields())
        feature.setGeometry(geometry)
        feature['id'] = symbol_name
        data_provider.addFeatures([feature])
        layer.updateExtents()

        category = QgsRendererCategoryV2(
            symbol_name,
            self.get_symbol(symbol_name),
            symbol_name)

        layer.rendererV2().addCategory(category)

    def draw_symbols_from_list(self, file_name):

        start_x = 2710000
        start_y = 1114000
        step_x = 0
        step_y = -20

        with open(file_name) as f:
            for i, symbol_name in enumerate(f.readlines()):
                self.draw_feature_with_symbol(
                    start_x + (step_x * i),
                    start_y + (step_y * i),
                    symbol_name)

    def save_pictures_from_list(self, file_name):
        size_x = 100
        size_y = 100
        output_directory = "/home/mario/workspace/repos/symbology-ti/ti-utils/output/png/"

        # TODO provare i vari parametri
        context = QgsRenderContext()
        context.setScaleFactor(20)
        
        with open(file_name) as f:
            for i, symbol_name in enumerate(f.readlines()):
                print(i)
                print(symbol_name)
                pixmap = QgsSymbolLayerV2Utils.symbolPreviewPixmap(
                    self.get_symbol(symbol_name), QSize(size_x, size_y), context)
                print(pixmap)
                filename = output_directory + symbol_name.strip() + ".png"
                print(filename)
                pixmap.save(filename, "PNG")

    def get_symbol(self, symbol_name):
        """Return the QgsSymbolV2 or None if not found"""

        style = QgsStyleV2().defaultStyle()
        return style.symbol(symbol_name.strip())


if __name__ in ['__main__', '__console__']:
    symbology_project = SymbologyProject()
    # symbology_project.create_layers()
    symbology_project.get_layers()

    symbology_project.draw_symbols_from_list(
        '/home/mario/workspace/repos/symbology-ti/ti-utils/fase2.txt')

    # symbology_project.save_pictures_from_list(
    #     '/home/mario/workspace/repos/symbology-ti/ti-utils/fase1.txt')
