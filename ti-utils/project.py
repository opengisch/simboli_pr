from qgis.core import (
    QgsStyleV2, QgsMapLayerRegistry, QgsVectorLayer, QgsFeature,
    QgsGeometry, QgsPoint, QgsCategorizedSymbolRendererV2,
    QgsRendererCategoryV2)


class SymbologyProject(object):

    def __init__(self):
        self.layer_points = None
        self.layer_lines = None
        self.layer_polygons = None

    def create_layers(self):

        self.layer_points = QgsVectorLayer(
            'Point?crs=epsg:2056&field=id:string(13)', 'Points', "memory")
        self.layer_points.setRendererV2(QgsCategorizedSymbolRendererV2('id'))

        self.layer_lines = QgsVectorLayer(
            'LineString?crs=epsg:2056&field=id:string(13)', 'Lines', "memory")
        self.layer_lines.setRendererV2(QgsCategorizedSymbolRendererV2('id'))

        self.layer_polygons = QgsVectorLayer(
            'Polygon?crs=epsg:2056&field=id:string(13)', 'Polygons', "memory")
        self.layer_polygons.setRendererV2(QgsCategorizedSymbolRendererV2('id'))

        QgsMapLayerRegistry.instance().addMapLayers(
            [self.layer_points, self.layer_lines, self.layer_polygons])

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

        feature.setGeometry(geometry)
        feature.setAttributes([symbol_name])
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
                    symbol_name.strip())

    def get_symbol(self, symbol_name):
        """Return the QgsSymbolV2 or None if not found"""

        style = QgsStyleV2().defaultStyle()
        return style.symbol(symbol_name)


if __name__ in ['__main__', '__console__']:
    symbology_project = SymbologyProject()
    symbology_project.create_layers()

#    symbology_project.draw_point_with_symbol(2710000, 1114000, 'P_26_120_0001')
    symbology_project.draw_symbols_from_list(
        '/home/mario/workspace/repos/symbology-ti/ti-utils/fase1.txt')



def draw_lines():
    # get the layer 
    # set in edit mode
    layer = iface.activeLayer()
    vpr = layer.dataProvider()
    
    features = []
    for i in range(10):
        f = QgsFeature()
        points = []
        points.append(QgsPoint(
            start_x + (step_x * i), start_y + (step_y * i)))
        points.append(QgsPoint(
            start_x + (step_x * i) + 10, start_y + (step_y * i)))
        line = QgsGeometry.fromPolyline(points)
        f.setGeometry(line)
        features.append(f)
    vpr.addFeatures(features)
    layer.updateExtents()

def draw_polygons():
    # get the layer 
    # set in edit mode
    layer = iface.activeLayer()
    vpr = layer.dataProvider()
    
    features = []
    for i in range(10):
        f = QgsFeature()
        points = []
        points.append(QgsPoint(
            start_x + (step_x * i), start_y + (step_y * i)))
        points.append(QgsPoint(
            start_x + (step_x * i) + 10, start_y + (step_y * i)))
        points.append(QgsPoint(
            start_x + (step_x * i) + 10, start_y + (step_y * i) + 10))
        points.append(QgsPoint(
            start_x + (step_x * i), start_y + (step_y * i) + 10))
        points.append(QgsPoint(
            start_x + (step_x * i), start_y + (step_y * i)))
        poly = QgsGeometry.fromPolygon([points])
        f.setGeometry(poly)
        features.append(f)
    vpr.addFeatures(features)
    layer.updateExtents()






