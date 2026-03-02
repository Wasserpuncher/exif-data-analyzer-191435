# EXIF Daten Analysator

Ein professionelles Python-Tool zur Extraktion und Analyse von EXIF (Exchangeable Image File Format) Mockup-Daten aus Bildern. Dieses Projekt nutzt objektorientierte Programmierung (OOP), Type-Hinting und umfassende Dokumentation, um eine robuste und benutzerfreundliche Lösung zum Verständnis von Bildmetadaten bereitzustellen.

## Inhaltsverzeichnis
- [Funktionen](#funktionen)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Projektstruktur](#projektstruktur)
- [Mitwirken](#mitwirken)
- [Lizenz](#lizenz)

## Funktionen
- **EXIF-Datenextraktion**: Liest und parst EXIF-Metadaten aus verschiedenen Bildformaten (JPEG, TIFF).
- **Datenanalyse**: Bietet Einblicke in gängige EXIF-Tags wie Kameramodell, Aufnahmedatum und GPS-Informationen.
- **Objektorientiertes Design**: Sauberer und modularer Code nach OOP-Prinzipien für einfache Erweiterung und Wartung.
- **Type-Hinting**: Verbesserte Code-Lesbarkeit und Wartbarkeit durch explizite Typannotationen.
- **Zweisprachige Dokumentation**: Englisches README und deutsches README für ein internationales Publikum.
- **Unit-Tests**: Umfassende Testsuite zur Sicherstellung von Zuverlässigkeit und Korrektheit.
- **CI/CD-Integration**: GitHub Actions Workflow für automatisierte Tests.

## Installation

1.  **Repository klonen**:
    ```bash
    git clone https://github.com/your-username/exif-data-analyzer.git
    cd exif-data-analyzer
    ```

2.  **Virtuelle Umgebung erstellen** (empfohlen):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Unter Windows: .venv\Scripts\activate
    ```

3.  **Abhängigkeiten installieren**:
    ```bash
    pip install -r requirements.txt
    ```

## Verwendung

Um EXIF-Daten aus einem Bild zu extrahieren und zu analysieren:

```bash
python main.py
```

Das `main.py`-Skript enthält ein Beispiel, wie man ein Dummy-Bild mit EXIF-Daten erstellt und dieses dann verarbeitet. Sie können `main.py` anpassen, um auf Ihre eigenen Bilddateien zu verweisen.

Beispielausgabe:

```
INFO:root:Creating a dummy image with EXIF data for demonstration...
INFO:root:Dummy image created at: dummy_image_with_exif.jpg
INFO:root:Extracting EXIF data from dummy_image_with_exif.jpg
INFO:root:EXIF Data:
{
    "Make": "DummyCamera",
    "Model": "DummyModel-X",
    "DateTimeOriginal": "2023:10:27 10:30:00",
    "GPSInfo": {
        "GPSLatitudeRef": "N",
        "GPSLatitude": [34, 1, 0],
        "GPSLongitudeRef": "W",
        "GPSLongitude": [118, 1, 0],
        "GPSTimeStamp": [10, 30, 0],
        "GPSProcessingMethod": "TEST_PROCESSOR"
    }
}
INFO:root:Analyzing EXIF data...
INFO:root:Analysis Results:
{
    "camera_model": "DummyCamera DummyModel-X",
    "has_gps_info": true,
    "capture_datetime": "2023:10:27 10:30:00"
}
```

## Projektstruktur

```
.
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI-Workflow
├── main.py                    # Hauptlogik für EXIF-Extraktion und -Analyse
├── test_main.py               # Unit-Tests für die Kernfunktionen
├── requirements.txt           # Python-Abhängigkeiten
├── README.md                  # Englische Projektdokumentation
├── README_de.md               # Deutsche Projektdokumentation
├── LICENSE                    # MIT-Lizenz
└── CONTRIBUTING.md            # Richtlinien für Mitwirkende
```

## Mitwirken

Wir freuen uns über Beiträge! Bitte beachten Sie die Datei [CONTRIBUTING.md](CONTRIBUTING.md) für Richtlinien, wie Sie zu diesem Projekt beitragen können.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Details finden Sie in der Datei [LICENSE](LICENSE).
