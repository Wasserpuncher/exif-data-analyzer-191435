# EXIF Data Analyzer

A professional Python tool designed for the extraction and analysis of EXIF (Exchangeable Image File Format) mockup data from images. This project leverages object-oriented programming (OOP), type-hinting, and comprehensive documentation to provide a robust and easy-to-use solution for understanding image metadata.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- **EXIF Data Extraction**: Reads and parses EXIF metadata from various image formats (JPEG, TIFF).
- **Data Analysis**: Provides insights into common EXIF tags such as camera model, capture date, and GPS information.
- **Object-Oriented Design**: Clean and modular code using OOP principles for easy extension and maintenance.
- **Type Hinting**: Enhanced code readability and maintainability with explicit type annotations.
- **Bilingual Documentation**: English README and German README for an international audience.
- **Unit Testing**: Comprehensive test suite to ensure reliability and correctness.
- **CI/CD Integration**: GitHub Actions workflow for automated testing.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/exif-data-analyzer.git
    cd exif-data-analyzer
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To extract and analyze EXIF data from an image:

```bash
python main.py
```

The `main.py` script includes an example of how to create a dummy image with EXIF data and then process it. You can modify `main.py` to point to your own image files.

Example output:

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

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow
├── main.py                    # Main logic for EXIF extraction and analysis
├── test_main.py               # Unit tests for the core functionalities
├── requirements.txt           # Python dependencies
├── README.md                  # English project documentation
├── README_de.md               # German project documentation
├── LICENSE                    # MIT License
└── CONTRIBUTING.md            # Guidelines for contributors
```

## Contributing

We welcome contributions! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
