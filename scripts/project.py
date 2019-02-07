import os

from qgis.PyQt.QtCore import QSettings, QVariant
from qgis.core import (
    QgsStyle, QgsVectorLayer, QgsCategorizedSymbolRenderer, QgsProject,
    QgsPointXY, QgsGeometry, QgsFeature, QgsRendererCategory,
    QgsField, QgsVectorLayerExporter, QgsWkbTypes,
    QgsCoordinateReferenceSystem, QgsFields)

from qgis.testing import start_app


class Project():
    """This class generates a demo QGIS project with a feature for each
    symbol. The result consist in a .qgs file and a geopackage file with the
    data."""

    def __init__(self, list_file, output_directory, project_name,
                 library_directory):
        """
        Constructor

        :param list_file: the path of a file containing the list of symbols
        to be included in the project.
        :param output_directory: the path of the directory where the project
        will be stored.
        :param project_name: the name of the created project.
        :param library_directory: path of the directory where the xml symbol
        library is located.
        """
        self.list_file = list_file
        self.output_directory = output_directory
        self.project_name = project_name
        self.library_directory = library_directory
        start_app()

    def run(self):
        """
        Start the project generation
        """
        self._import_library_into_qgis()
        layers = self._create_gpkg_with_layers()
        QgsProject.instance().addMapLayers(list(layers))
        QgsProject.instance().setCrs(QgsCoordinateReferenceSystem('EPSG:2056'))
        self._add_features(*layers)
        QgsProject.instance().write(
            os.path.join(self.output_directory, self.project_name))

    def _import_library_into_qgis(self):
        s = QSettings()
        svg_paths = []
        svg_paths.append(os.path.join(self.library_directory, 'svg/'))
        s.setValue('svg/searchPathsForSVG', svg_paths)

        style = QgsStyle.defaultStyle()
        style.importXml(
            os.path.join(self.library_directory, 'libreria.xml'))

    def _create_gpkg_with_layers(self):
        gpkg_file = os.path.join(self.output_directory, 'layers.gpkg')

        options = {}
        options['driverName'] = 'GPKG'
        options['layerName'] = 'points'
        fields = QgsFields()
        fields.append(QgsField('id', QVariant.String))
        QgsVectorLayerExporter(
            gpkg_file, "ogr", fields, QgsWkbTypes.Point,
            QgsCoordinateReferenceSystem('EPSG:2056'), False, options)
        layer_points = QgsVectorLayer(
            '{}|layername=points'.format(gpkg_file), 'points', 'ogr')

        options['update'] = True
        options['layerName'] = 'lines'
        fields = QgsFields()
        fields.append(QgsField('id', QVariant.String))
        QgsVectorLayerExporter(
            gpkg_file, "ogr", fields, QgsWkbTypes.LineString,
            QgsCoordinateReferenceSystem('EPSG:2056'), False, options)
        layer_lines = QgsVectorLayer(
            '{}|layername=lines'.format(gpkg_file), 'lines', 'ogr')

        options['update'] = True
        options['layerName'] = 'polygons'
        fields = QgsFields()
        fields.append(QgsField('id', QVariant.String))
        QgsVectorLayerExporter(
            gpkg_file, "ogr", fields, QgsWkbTypes.Polygon,
            QgsCoordinateReferenceSystem('EPSG:2056'), False, options)
        layer_polygons = QgsVectorLayer(
            '{}|layername=polygons'.format(gpkg_file), 'polygons', 'ogr')

        layer_points.setRenderer(QgsCategorizedSymbolRenderer('id'))
        layer_lines.setRenderer(QgsCategorizedSymbolRenderer('id'))
        layer_polygons.setRenderer(QgsCategorizedSymbolRenderer('id'))

        return layer_points, layer_lines, layer_polygons

    def _add_features(self, layer_points, layer_lines, layer_polygons):
        start_x = 2710000
        start_y = 1114000
        step_x = 0
        step_y = -20
        style = QgsStyle.defaultStyle()

        with open(self.list_file) as f:
            for i, symbol_name in enumerate(f.readlines()):
                pos_x = start_x + (step_x * i)
                pos_y = start_y + (step_y * i)

                if symbol_name.startswith('P_'):
                    layer = layer_points
                    geometry = QgsGeometry.fromPointXY(
                        QgsPointXY(pos_x, pos_y))
                elif symbol_name.startswith('L_'):
                    layer = layer_lines
                    points = []
                    points.append(QgsPointXY(pos_x, pos_y))
                    points.append(QgsPointXY(pos_x + 200, pos_y))
                    geometry = QgsGeometry.fromPolylineXY(points)
                elif symbol_name.startswith('S_'):
                    layer = layer_polygons
                    points = []
                    points.append(QgsPointXY(pos_x, pos_y))
                    points.append(QgsPointXY(pos_x + 200, pos_y))
                    points.append(QgsPointXY(pos_x + 200, pos_y + 10))
                    points.append(QgsPointXY(pos_x, pos_y + 10))
                    points.append(QgsPointXY(pos_x, pos_y))
                    geometry = QgsGeometry.fromPolygonXY([points])

                data_provider = layer.dataProvider()
                feature = QgsFeature()
                feature.setFields(layer.fields())
                feature.setGeometry(geometry)
                feature['id'] = symbol_name
                data_provider.addFeatures([feature])
                layer.updateExtents()

                category = QgsRendererCategory(
                    symbol_name,
                    style.symbol(symbol_name.strip()),
                    symbol_name)

                layer.renderer().addCategory(category)


if __name__ == '__main__':

    main_dir_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.pardir)

    project = Project(
        os.path.join(main_dir_path, 'scripts/fase2.txt'),
        os.path.join(main_dir_path, 'result/qgis_project'),
        'libreria.qgs',
        os.path.join(main_dir_path, 'result/libreria'))
    project.run()
