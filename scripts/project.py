import os

from qgis.PyQt.QtCore import QSettings, QVariant
from qgis.core import (
    QgsStyle, QgsVectorLayer, QgsCategorizedSymbolRenderer, QgsProject,
    QgsPointXY, QgsGeometry, QgsFeature, QgsRendererCategory,
    QgsField, QgsVectorLayerExporter, QgsWkbTypes,
    QgsCoordinateReferenceSystem, QgsFields)

from qgis.testing import start_app

start_app()
main_dir_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir)

s = QSettings()
svg_paths = []
svg_paths.append(os.path.join(main_dir_path, 'result/libreria/svg/'))
s.setValue('svg/searchPathsForSVG', svg_paths)

style = QgsStyle.defaultStyle()
style.importXml(os.path.join(main_dir_path, 'result/libreria/libreria.xml'))

gpkg_file = os.path.join(main_dir_path, 'result/qgis_project', 'layers.gpkg')

options = {}
options['driverName'] = 'GPKG'
options['layerName'] = 'points'

fields = QgsFields()
fields.append(QgsField('id', QVariant.String))

QgsVectorLayerExporter(
    gpkg_file, "ogr", fields, QgsWkbTypes.Point,
    QgsCoordinateReferenceSystem('EPSG:2056'), False, options)

layer_points = QgsVectorLayer(
    '{}|layername=points'.format(gpkg_file),
    'points',
    'ogr')
options['update'] = True
options['layerName'] = 'lines'
fields = QgsFields()
fields.append(QgsField('id', QVariant.String))

QgsVectorLayerExporter(
    gpkg_file, "ogr", fields, QgsWkbTypes.LineString,
    QgsCoordinateReferenceSystem('EPSG:2056'), False, options)

layer_lines = QgsVectorLayer(
    '{}|layername=lines'.format(gpkg_file),
    'lines',
    'ogr')
options['update'] = True
options['layerName'] = 'polygons'
fields = QgsFields()
fields.append(QgsField('id', QVariant.String))

QgsVectorLayerExporter(
    gpkg_file, "ogr", fields, QgsWkbTypes.Polygon,
    QgsCoordinateReferenceSystem('EPSG:2056'), False, options)

layer_polygons = QgsVectorLayer(
    '{}|layername=polygons'.format(gpkg_file),
    'polygons',
    'ogr')

layer_points.setRenderer(QgsCategorizedSymbolRenderer('id'))
layer_lines.setRenderer(QgsCategorizedSymbolRenderer('id'))
layer_polygons.setRenderer(QgsCategorizedSymbolRenderer('id'))

QgsProject.instance().addMapLayers([layer_points, layer_lines, layer_polygons])
QgsProject.instance().setCrs(QgsCoordinateReferenceSystem('EPSG:2056'))

file_name = os.path.join(main_dir_path, 'scripts/fase2.txt')

start_x = 2710000
start_y = 1114000
step_x = 0
step_y = -20

with open(file_name) as f:
    for i, symbol_name in enumerate(f.readlines()):
        pos_x = start_x + (step_x * i)
        pos_y = start_y + (step_y * i)

        if symbol_name.startswith('P_'):
            layer = layer_points
            geometry = QgsGeometry.fromPointXY(QgsPointXY(pos_x, pos_y))
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

QgsProject.instance().write(
    os.path.join(main_dir_path, 'result/qgis_project', 'libreria.qgs'))
