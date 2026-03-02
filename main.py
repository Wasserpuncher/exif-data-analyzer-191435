import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union

# Import Pillow (PIL) for image processing and EXIF handling
# Importiere Pillow (PIL) für Bildverarbeitung und EXIF-Handhabung
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Configure logging for better output management
# Konfiguriere Logging für besseres Ausgabemanagement
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def _create_dummy_image_with_exif(output_path: Path, include_gps: bool = True, include_no_exif: bool = False) -> None:
    """
    Creates a dummy JPEG image with mock EXIF data for demonstration and testing purposes.
    Erstellt ein Dummy-JPEG-Bild mit Mock-EXIF-Daten zu Demonstrations- und Testzwecken.

    Args:
        output_path (Path): The path where the dummy image will be saved.
                            Der Pfad, unter dem das Dummy-Bild gespeichert wird.
        include_gps (bool): Whether to include GPS info in the EXIF data.
                            Ob GPS-Informationen in den EXIF-Daten enthalten sein sollen.
        include_no_exif (bool): If True, creates an image with no EXIF data.
                                Wenn True, wird ein Bild ohne EXIF-Daten erstellt.
    """
    try:
        # Create a simple white image
        # Erstelle ein einfaches weißes Bild
        img = Image.new('RGB', (100, 100), color = 'white')

        if include_no_exif:
            # Save without any EXIF data
            # Speichern ohne EXIF-Daten
            img.save(output_path, "jpeg")
            logger.info(f"Dummy image with NO EXIF created at: {output_path}")
            return

        # Prepare EXIF data using PIL.Exif
        # EXIF-Daten mit PIL.Exif vorbereiten
        exif_obj = Image.Exif()

        # Common EXIF tags
        # Gängige EXIF-Tags
        exif_obj[0x010F] = "DummyCamera"        # Make / Hersteller
        exif_obj[0x0110] = "DummyModel-X"       # Model / Modell
        exif_obj[0x9003] = "2023:10:27 10:30:00" # DateTimeOriginal / Original-Aufnahmedatum
        exif_obj[0x920A] = 100                  # FocalLength / Brennweite
        exif_obj[0x8827] = 100                  # ISOSpeedRatings / ISO-Empfindlichkeit

        # Add GPS info if requested
        # GPS-Informationen hinzufügen, falls angefordert
        if include_gps:
            # GPSInfo values are stored as tuples of (numerator, denominator) for fractions,
            # or direct values for strings/integers.
            # GPSInfo-Werte werden als Tupel von (Zähler, Nenner) für Brüche gespeichert,
            # oder direkte Werte für Strings/Integer.
            # Pillow's `Exif` object can take numbers directly for tags that expect them.
            # The GPSInfo tag (0x8825) is special. PIL.Exif can take a sub-Exif object for it.
            # Der GPSInfo-Tag (0x8825) ist speziell. PIL.Exif kann ein Unter-Exif-Objekt dafür aufnehmen.
            gps_exif_sub_obj = Image.Exif()
            gps_exif_sub_obj[0x0001] = "N" # GPSLatitudeRef
            gps_exif_sub_obj[0x0002] = (34, 1, 0) # GPSLatitude: 34 degrees N (simplified representation)
            gps_exif_sub_obj[0x0003] = "W" # GPSLongitudeRef
            gps_exif_sub_obj[0x0004] = (118, 1, 0) # GPSLongitude: 118 degrees W (simplified representation)
            gps_exif_sub_obj[0x0007] = (10, 30, 0) # GPSTimeStamp: 10:30:00
            gps_exif_sub_obj[0x001B] = "TEST_PROCESSOR" # GPSProcessingMethod
            
            # Merge GPS tags into the main EXIF object under the GPS IFD
            # Füge GPS-Tags in das Haupt-EXIF-Objekt unter dem GPS IFD ein
            exif_obj.add_all(gps_exif_sub_obj._dict, "GPS")

        # Save the image with EXIF data
        # Speichere das Bild mit EXIF-Daten
        # .tobytes() generates the EXIF segment in JPEG format
        # .tobytes() generiert das EXIF-Segment im JPEG-Format
        img.save(output_path, "jpeg", exif=exif_obj.tobytes())
        logger.info(f"Dummy image with EXIF created at: {output_path}")
    except Exception as e:
        logger.error(f"Error creating dummy image at {output_path}: {e}")
        # Re-raise for testing purposes if this function is used in tests
        # Erneut auslösen für Testzwecke, wenn diese Funktion in Tests verwendet wird
        raise

class ExifDataExtractor:
    """
    A class to extract EXIF (Exchangeable Image File Format) data from an image file.
    Eine Klasse zum Extrahieren von EXIF (Exchangeable Image File Format)-Daten aus einer Bilddatei.
    """

    def __init__(self, image_path: Path) -> None:
        """
        Initializes the ExifDataExtractor with the path to the image.
        Initialisiert den ExifDataExtractor mit dem Pfad zum Bild.

        Args:
            image_path (Path): The path to the image file.
                               Der Pfad zur Bilddatei.
        """
        if not isinstance(image_path, Path):
            raise TypeError("image_path must be a pathlib.Path object.")
            # image_path muss ein pathlib.Path-Objekt sein.
        self.image_path: Path = image_path
        logger.debug(f"Extractor initialized for image: {self.image_path}")
        # Extractor für Bild initialisiert: {self.image_path}

    def _get_if_exists(self, data: Dict[int, Any], key: int) -> Optional[Any]:
        """
        Helper method to safely get a value from a dictionary if the key exists.
        Hilfsmethode, um einen Wert sicher aus einem Wörterbuch abzurufen, falls der Schlüssel existiert.

        Args:
            data (Dict[int, Any]): The dictionary to query.
                                   Das abzufragende Wörterbuch.
            key (int): The key to look for.
                       Der zu suchende Schlüssel.

        Returns:
            Optional[Any]: The value associated with the key, or None if the key is not found.
                           Der mit dem Schlüssel verbundene Wert, oder None, wenn der Schlüssel nicht gefunden wird.
        """
        return data.get(key)

    def extract_exif_data(self) -> Dict[str, Any]:
        """
        Extracts EXIF data from the image file specified during initialization.
        Extrahiert EXIF-Daten aus der während der Initialisierung angegebenen Bilddatei.

        Returns:
            Dict[str, Any]: A dictionary containing the extracted EXIF data with human-readable tags.
                            Ein Wörterbuch, das die extrahierten EXIF-Daten mit menschenlesbaren Tags enthält.
                            Returns an empty dictionary if no EXIF data is found or an error occurs.
                            Gibt ein leeres Wörterbuch zurück, wenn keine EXIF-Daten gefunden werden oder ein Fehler auftritt.
        """
        if not self.image_path.exists():
            logger.warning(f"Image file not found: {self.image_path}")
            # Bilddatei nicht gefunden: {self.image_path}
            return {}
        if not self.image_path.is_file():
            logger.warning(f"Path is not a file: {self.image_path}")
            # Pfad ist keine Datei: {self.image_path}
            return {}

        exif_data: Dict[str, Any] = {}
        try:
            with Image.open(self.image_path) as img:
                # Use _getexif() to get the raw EXIF data dictionary
                # Verwende _getexif(), um das rohe EXIF-Daten-Wörterbuch zu erhalten
                raw_exif = img._getexif()
                if raw_exif is None:
                    logger.info(f"No EXIF data found in {self.image_path}")
                    # Keine EXIF-Daten gefunden in {self.image_path}
                    return {}

                for tag_id, value in raw_exif.items():
                    # Get human-readable tag name
                    # Hole den menschenlesbaren Tag-Namen
                    tag_name = TAGS.get(tag_id, tag_id)
                    if tag_name == 'GPSInfo':
                        # GPSInfo is a sub-dictionary, needs special handling
                        # GPSInfo ist ein Unter-Wörterbuch, benötigt spezielle Behandlung
                        gps_info = {}
                        for gps_tag_id, gps_value in value.items():
                            gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_info[str(gps_tag_name)] = gps_value
                        exif_data[str(tag_name)] = gps_info
                    else:
                        exif_data[str(tag_name)] = value
            logger.info(f"Successfully extracted EXIF data from {self.image_path}")
            # EXIF-Daten erfolgreich extrahiert aus {self.image_path}
            return exif_data
        except IOError as e:
            logger.error(f"Could not open or read image file {self.image_path}: {e}")
            # Bilddatei {self.image_path} konnte nicht geöffnet oder gelesen werden: {e}
            return {}
        except Exception as e:
            logger.error(f"An unexpected error occurred during EXIF extraction from {self.image_path}: {e}")
            # Ein unerwarteter Fehler ist während der EXIF-Extraktion aus {self.image_path} aufgetreten: {e}
            return {}

class ExifAnalyzer:
    """
    A class to analyze extracted EXIF data and provide structured insights.
    Eine Klasse zur Analyse extrahierter EXIF-Daten und zur Bereitstellung strukturierter Einblicke.
    """

    def __init__(self, exif_data: Dict[str, Any]) -> None:
        """
        Initializes the ExifAnalyzer with extracted EXIF data.
        Initialisiert den ExifAnalyzer mit extrahierten EXIF-Daten.

        Args:
            exif_data (Dict[str, Any]): A dictionary of EXIF data, typically from ExifDataExtractor.
                                        Ein Wörterbuch mit EXIF-Daten, typischerweise vom ExifDataExtractor.
        """
        if not isinstance(exif_data, dict):
            raise TypeError("exif_data must be a dictionary.")
            # exif_data muss ein Wörterbuch sein.
        self.exif_data: Dict[str, Any] = exif_data
        logger.debug("Analyzer initialized with EXIF data.")
        # Analyzer mit EXIF-Daten initialisiert.

    def get_camera_model(self) -> Optional[str]:
        """
        Retrieves the camera make and model from the EXIF data.
        Ruft den Kamerahersteller und das Modell aus den EXIF-Daten ab.

        Returns:
            Optional[str]: A string representing the camera model (e.g., "Canon EOS 5D Mark IV"),
                           or None if not found.
                           Ein String, der das Kameramodell darstellt (z.B. "Canon EOS 5D Mark IV"),
                           oder None, wenn nicht gefunden.
        """
        make = self.exif_data.get('Make')
        model = self.exif_data.get('Model')

        if make and model:
            return f"{make} {model}"
        elif make:
            return str(make)
        elif model:
            return str(model)
        return None

    def has_gps_info(self) -> bool:
        """
        Checks if the EXIF data contains GPS (Global Positioning System) information.
        Überprüft, ob die EXIF-Daten GPS-Informationen (Global Positioning System) enthalten.

        Returns:
            bool: True if GPS info is present, False otherwise.
                  True, wenn GPS-Informationen vorhanden sind, sonst False.
        """
        return 'GPSInfo' in self.exif_data and bool(self.exif_data['GPSInfo'])

    def get_capture_datetime(self) -> Optional[str]:
        """
        Retrieves the original capture date and time from the EXIF data.
        Ruft das ursprüngliche Aufnahme-Datum und die Uhrzeit aus den EXIF-Daten ab.

        Returns:
            Optional[str]: A string representing the capture date and time (e.g., "YYYY:MM:DD HH:MM:SS"),
                           or None if not found.
                           Ein String, der das Aufnahme-Datum und die Uhrzeit darstellt (z.B. "JJJJ:MM:TT HH:MM:SS"),
                           oder None, wenn nicht gefunden.
        """
        return self.exif_data.get('DateTimeOriginal')

    def analyze(self) -> Dict[str, Any]:
        """
        Performs a comprehensive analysis of the EXIF data.
        Führt eine umfassende Analyse der EXIF-Daten durch.

        Returns:
            Dict[str, Any]: A dictionary containing various analysis results.
                            Ein Wörterbuch, das verschiedene Analyseergebnisse enthält.
        """
        analysis_results: Dict[str, Any] = {
            "camera_model": self.get_camera_model(),
            "has_gps_info": self.has_gps_info(),
            "capture_datetime": self.get_capture_datetime(),
            # Add more analysis points as needed
            # Fügen Sie bei Bedarf weitere Analysepunkte hinzu
        }
        logger.debug("EXIF data analysis complete.")
        # EXIF-Datenanalyse abgeschlossen.
        return analysis_results

def main() -> None:
    """
    Main function to demonstrate EXIF data extraction and analysis.
    Hauptfunktion zur Demonstration der EXIF-Datenextraktion und -analyse.
    It creates a dummy image, extracts its EXIF data, and performs analysis.
    Sie erstellt ein Dummy-Bild, extrahiert dessen EXIF-Daten und führt eine Analyse durch.
    """
    logger.info("Starting EXIF Data Analyzer demonstration.")
    # Starte EXIF-Daten-Analysator-Demonstration.

    dummy_image_path = Path("dummy_image_with_exif.jpg")

    try:
        # Create a dummy image for demonstration
        # Erstelle ein Dummy-Bild zur Demonstration
        logger.info("Creating a dummy image with EXIF data for demonstration...")
        # Erstelle ein Dummy-Bild mit EXIF-Daten zur Demonstration...
        _create_dummy_image_with_exif(dummy_image_path)

        # 1. Extract EXIF Data
        # 1. EXIF-Daten extrahieren
        logger.info(f"Extracting EXIF data from {dummy_image_path}")
        # Extrahiere EXIF-Daten aus {dummy_image_path}
        extractor = ExifDataExtractor(dummy_image_path)
        extracted_data = extractor.extract_exif_data()

        logger.info("EXIF Data:")
        # EXIF-Daten:
        print(json.dumps(extracted_data, indent=4))

        # 2. Analyze EXIF Data
        # 2. EXIF-Daten analysieren
        if extracted_data:
            logger.info("Analyzing EXIF data...")
            # Analysiere EXIF-Daten...
            analyzer = ExifAnalyzer(extracted_data)
            analysis_results = analyzer.analyze()

            logger.info("Analysis Results:")
            # Analyseergebnisse:
            print(json.dumps(analysis_results, indent=4))
        else:
            logger.warning("No EXIF data extracted, skipping analysis.")
            # Keine EXIF-Daten extrahiert, Analyse wird übersprungen.

    except Exception as e:
        logger.critical(f"An error occurred during the main execution: {e}")
        # Ein Fehler ist während der Hauptausführung aufgetreten: {e}
    finally:
        # Clean up the dummy image
        # Bereinige das Dummy-Bild
        if dummy_image_path.exists():
            dummy_image_path.unlink()
            logger.info(f"Cleaned up dummy image: {dummy_image_path}")
            # Dummy-Bild bereinigt: {dummy_image_path}
    
    logger.info("EXIF Data Analyzer demonstration finished.")
    # EXIF-Daten-Analysator-Demonstration beendet.

if __name__ == "__main__":
    main()
