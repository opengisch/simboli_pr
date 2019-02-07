import os
import unittest


class TestResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.main_dir_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), os.pardir)

    def test_directory_structure(self):
        self.assertTrue(
            os.path.isdir(os.path.join(self.main_dir_path, 'result')))
        self.assertTrue(
            os.path.isdir(
                os.path.join(self.main_dir_path, 'result', 'libreria')))
        self.assertTrue(
            os.path.isdir(
                os.path.join(self.main_dir_path, 'result', 'libreria', 'svg')))
        self.assertTrue(
            os.path.isdir(os.path.join(self.main_dir_path, 'result', 'png')))
        self.assertTrue(
            os.path.isdir(
                os.path.join(self.main_dir_path, 'result', 'qgis_project')))

    def test_library_xml_is_created(self):
        filepath = os.path.join(
            self.main_dir_path, 'result', 'libreria', 'libreria.xml')

        self.assertTrue(os.path.isfile(filepath))
        self.assertGreater(os.path.getsize(filepath), 2500000)

    def test_svg_are_created(self):
        dirpath = os.path.join(
            self.main_dir_path, 'result', 'libreria', 'svg')
        self.assertGreater(
            len([name for name in os.listdir(dirpath)
                 if name.endswith('.svg')]),
            250)

    def test_png_are_created(self):
        dirpath = os.path.join(
            self.main_dir_path, 'result', 'png')
        self.assertEqual(
            len([name for name in os.listdir(dirpath)
                 if name.endswith('.png')]),
            1203)

    def test_qgis_project_is_created(self):
        filepath = os.path.join(
            self.main_dir_path, 'result', 'qgis_project', 'libreria.qgs')

        self.assertTrue(os.path.isfile(filepath))
        self.assertGreater(os.path.getsize(filepath), 2500000)

    def test_gpkg_is_created(self):
        filepath = os.path.join(
            self.main_dir_path, 'result', 'qgis_project', 'layers.gpkg')

        self.assertTrue(os.path.isfile(filepath))
        self.assertGreater(os.path.getsize(filepath), 250000)

    def test_zip_file_is_created(self):
        filepath = os.path.join(
            self.main_dir_path, 'result', 'libreria.zip')

        self.assertTrue(os.path.isfile(filepath))
        self.assertGreater(os.path.getsize(filepath), 1000000)


if __name__ == '__main__':
    unittest.main()
