import unittest
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Import the classes and helper function from main.py
# Importiere die Klassen und Hilfsfunktionen aus main.py
from main import ExifDataExtractor, ExifAnalyzer, _create_dummy_image_with_exif

# Suppress logging during tests for cleaner output, or set to WARNING/ERROR
# Unterdrücke Logging während der Tests für eine sauberere Ausgabe, oder setze auf WARNING/ERROR
logging.basicConfig(level=logging.CRITICAL)

class TestExifDataExtractor(unittest.TestCase):
    """
    Unit tests for the ExifDataExtractor class.
    Unit-Tests für die Klasse ExifDataExtractor.
    """
    DUMMY_IMAGE_WITH_EXIF = Path("test_image_with_exif.jpg")
    DUMMY_IMAGE_NO_EXIF = Path("test_image_no_exif.jpg")
    DUMMY_NON_IMAGE_FILE = Path("test_non_image.txt")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up test resources: create dummy image files with and without EXIF data.
        Richte Testressourcen ein: Erstelle Dummy-Bilddateien mit und ohne EXIF-Daten.
        """
        # Create dummy image with EXIF data
        # Erstelle Dummy-Bild mit EXIF-Daten
        _create_dummy_image_with_exif(cls.DUMMY_IMAGE_WITH_EXIF, include_gps=True)
        # Create dummy image without EXIF data
        # Erstelle Dummy-Bild ohne EXIF-Daten
        _create_dummy_image_with_exif(cls.DUMMY_IMAGE_NO_EXIF, include_no_exif=True)
        # Create a dummy non-image file
        # Erstelle eine Dummy-Nicht-Bilddatei
        cls.DUMMY_NON_IMAGE_FILE.write_text("This is not an image file.")
        
        # Ensure files exist for tests
        # Stelle sicher, dass Dateien für Tests existieren
        assert cls.DUMMY_IMAGE_WITH_EXIF.exists()
        assert cls.DUMMY_IMAGE_NO_EXIF.exists()
        assert cls.DUMMY_NON_IMAGE_FILE.exists()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up test resources: remove dummy image files.
        Bereinige Testressourcen: Entferne Dummy-Bilddateien.
        """
        if cls.DUMMY_IMAGE_WITH_EXIF.exists():
            cls.DUMMY_IMAGE_WITH_EXIF.unlink()
        if cls.DUMMY_IMAGE_NO_EXIF.exists():
            cls.DUMMY_IMAGE_NO_EXIF.unlink()
        if cls.DUMMY_NON_IMAGE_FILE.exists():
            cls.DUMMY_NON_IMAGE_FILE.unlink()

    def test_init_type_error(self) -> None:
        """
        Test that initialization with a non-Path object raises a TypeError.
        Teste, dass die Initialisierung mit einem Nicht-Path-Objekt einen TypeError auslöst.
        """
        with self.assertRaises(TypeError):
            ExifDataExtractor("not_a_path_object")

    def test_extract_valid_exif(self) -> None:
        """
        Test extraction from an image with valid EXIF data.
        Teste die Extraktion aus einem Bild mit gültigen EXIF-Daten.
        """
        extractor = ExifDataExtractor(self.DUMMY_IMAGE_WITH_EXIF)
        exif_data = extractor.extract_exif_data()

        self.assertIsInstance(exif_data, dict)
        self.assertGreater(len(exif_data), 0)
        self.assertIn('Make', exif_data)
        self.assertEqual(exif_data['Make'], "DummyCamera")
        self.assertIn('Model', exif_data)
        self.assertEqual(exif_data['Model'], "DummyModel-X")
        self.assertIn('DateTimeOriginal', exif_data)
        self.assertIn('GPSInfo', exif_data)
        self.assertIsInstance(exif_data['GPSInfo'], dict)
        self.assertIn('GPSLatitude', exif_data['GPSInfo'])
        self.assertEqual(exif_data['GPSInfo']['GPSLatitude'], (34, 1, 0))

    def test_extract_no_exif(self) -> None:
        """
        Test extraction from an image with no EXIF data.
        Teste die Extraktion aus einem Bild ohne EXIF-Daten.
        """
        extractor = ExifDataExtractor(self.DUMMY_IMAGE_NO_EXIF)
        exif_data = extractor.extract_exif_data()

        self.assertIsInstance(exif_data, dict)
        self.assertEqual(len(exif_data), 0)

    def test_extract_non_existent_file(self) -> None:
        """
        Test extraction from a non-existent file path.
        Teste die Extraktion aus einem nicht existierenden Dateipfad.
        """
        non_existent_path = Path("non_existent_image.jpg")
        extractor = ExifDataExtractor(non_existent_path)
        exif_data = extractor.extract_exif_data()

        self.assertIsInstance(exif_data, dict)
        self.assertEqual(len(exif_data), 0)

    def test_extract_non_image_file(self) -> None:
        """
        Test extraction from a file that is not an image.
        Teste die Extraktion aus einer Datei, die kein Bild ist.
        """
        extractor = ExifDataExtractor(self.DUMMY_NON_IMAGE_FILE)
        exif_data = extractor.extract_exif_data()

        self.assertIsInstance(exif_data, dict)
        self.assertEqual(len(exif_data), 0) # Should return empty dict as it can't be opened as image

class TestExifAnalyzer(unittest.TestCase):
    """
    Unit tests for the ExifAnalyzer class.
    Unit-Tests für die Klasse ExifAnalyzer.
    """

    def test_init_type_error(self) -> None:
        """
        Test that initialization with a non-dictionary object raises a TypeError.
        Teste, dass die Initialisierung mit einem Nicht-Wörterbuch-Objekt einen TypeError auslöst.
        """
        with self.assertRaises(TypeError):
            ExifAnalyzer("not_a_dict")

    def test_get_camera_model_full(self) -> None:
        """
        Test retrieving camera model when both Make and Model are present.
        Teste das Abrufen des Kameramodells, wenn sowohl Hersteller als auch Modell vorhanden sind.
        """
        exif_data = {"Make": "Canon", "Model": "EOS 5D Mark IV"}
        analyzer = ExifAnalyzer(exif_data)
        self.assertEqual(analyzer.get_camera_model(), "Canon EOS 5D Mark IV")

    def test_get_camera_model_only_make(self) -> None:
        """
        Test retrieving camera model when only Make is present.
        Teste das Abrufen des Kameramodells, wenn nur der Hersteller vorhanden ist.
        """
        exif_data = {"Make": "Nikon"}
        analyzer = ExifAnalyzer(exif_data)
        self.assertEqual(analyzer.get_camera_model(), "Nikon")

    def test_get_camera_model_only_model(self) -> None:
        """
        Test retrieving camera model when only Model is present.
        Teste das Abrufen des Kameramodells, wenn nur das Modell vorhanden ist.
        """
        exif_data = {"Model": "X-T4"}
        analyzer = ExifAnalyzer(exif_data)
        self.assertEqual(analyzer.get_camera_model(), "X-T4")

    def test_get_camera_model_none(self) -> None:
        """
        Test retrieving camera model when neither Make nor Model are present.
        Teste das Abrufen des Kameramodells, wenn weder Hersteller noch Modell vorhanden sind.
        """
        exif_data = {"DateTimeOriginal": "2023:01:01 12:00:00"}
        analyzer = ExifAnalyzer(exif_data)
        self.assertIsNone(analyzer.get_camera_model())

    def test_has_gps_info_true(self) -> None:
        """
        Test checking for GPS info when it is present.
        Teste die Überprüfung auf GPS-Informationen, wenn diese vorhanden sind.
        """
        exif_data = {"GPSInfo": {"GPSLatitude": (10, 20, 30)}}
        analyzer = ExifAnalyzer(exif_data)
        self.assertTrue(analyzer.has_gps_info())

    def test_has_gps_info_false_empty_dict(self) -> None:
        """
        Test checking for GPS info when the GPSInfo dictionary is empty.
        Teste die Überprüfung auf GPS-Informationen, wenn das GPSInfo-Wörterbuch leer ist.
        """
        exif_data = {"GPSInfo": {}}
        analyzer = ExifAnalyzer(exif_data)
        self.assertFalse(analyzer.has_gps_info())

    def test_has_gps_info_false_not_present(self) -> None:
        """
        Test checking for GPS info when it is not present at all.
        Teste die Überprüfung auf GPS-Informationen, wenn diese überhaupt nicht vorhanden sind.
        """
        exif_data = {"Make": "Dummy"}
        analyzer = ExifAnalyzer(exif_data)
        self.assertFalse(analyzer.has_gps_info())

    def test_get_capture_datetime_present(self) -> None:
        """
        Test retrieving capture datetime when it is present.
        Teste das Abrufen des Aufnahme-Datums und der Uhrzeit, wenn diese vorhanden sind.
        """
        datetime_str = "2023:10:27 10:30:00"
        exif_data = {"DateTimeOriginal": datetime_str}
        analyzer = ExifAnalyzer(exif_data)
        self.assertEqual(analyzer.get_capture_datetime(), datetime_str)

    def test_get_capture_datetime_none(self) -> None:
        """
        Test retrieving capture datetime when it is not present.
        Teste das Abrufen des Aufnahme-Datums und der Uhrzeit, wenn diese nicht vorhanden sind.
        """
        exif_data = {"Make": "Dummy"}
        analyzer = ExifAnalyzer(exif_data)
        self.assertIsNone(analyzer.get_capture_datetime())

    def test_analyze_complete_data(self) -> None:
        """
        Test comprehensive analysis with complete EXIF data.
        Teste die umfassende Analyse mit vollständigen EXIF-Daten.
        """
        exif_data = {
            "Make": "DummyCamera",
            "Model": "DummyModel-X",
            "DateTimeOriginal": "2023:10:27 10:30:00",
            "GPSInfo": {
                "GPSLatitudeRef": "N",
                "GPSLatitude": (34, 1, 0),
                "GPSLongitudeRef": "W",
                "GPSLongitude": (118, 1, 0),
                "GPSTimeStamp": (10, 30, 0),
                "GPSProcessingMethod": "TEST_PROCESSOR"
            }
        }
        analyzer = ExifAnalyzer(exif_data)
        results = analyzer.analyze()

        self.assertIsInstance(results, dict)
        self.assertEqual(results["camera_model"], "DummyCamera DummyModel-X")
        self.assertTrue(results["has_gps_info"])
        self.assertEqual(results["capture_datetime"], "2023:10:27 10:30:00")

    def test_analyze_partial_data(self) -> None:
        """
        Test comprehensive analysis with partial EXIF data.
        Teste die umfassende Analyse mit teilweisen EXIF-Daten.
        """
        exif_data = {
            "Make": "PartialCam",
            "DateTimeOriginal": "2022:01:01 00:00:00",
        }
        analyzer = ExifAnalyzer(exif_data)
        results = analyzer.analyze()

        self.assertIsInstance(results, dict)
        self.assertEqual(results["camera_model"], "PartialCam")
        self.assertFalse(results["has_gps_info"])
        self.assertEqual(results["capture_datetime"], "2022:01:01 00:00:00")

    def test_analyze_empty_data(self) -> None:
        """
        Test comprehensive analysis with empty EXIF data.
        Teste die umfassende Analyse mit leeren EXIF-Daten.
        """
        exif_data = {}
        analyzer = ExifAnalyzer(exif_data)
        results = analyzer.analyze()

        self.assertIsInstance(results, dict)
        self.assertIsNone(results["camera_model"])
        self.assertFalse(results["has_gps_info"])
        self.assertIsNone(results["capture_datetime"])

if __name__ == '__main__':
    unittest.main()
