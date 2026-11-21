# SWYNEX Python Automation Tool

## Python File Organizer

A Python-based automation application that organizes files into separate folders according to their file extensions.

## Features

- Automatic file organization
- Document and image sorting
- Audio and video sorting
- Spreadsheet and presentation sorting
- Duplicate filename protection
- Preview mode
- CSV report generation
- Activity logging
- Exception handling
- Automated unit testing

## Technologies Used

- Python 3.13
- pathlib
- os
- shutil
- csv
- logging
- argparse
- unittest

## Project Structure

```text
SWYNEX-Python-Automation-Tool/
│
├── main.py
├── file_organizer/
│   ├── __init__.py
│   └── organizer.py
├── tests/
│   ├── __init__.py
│   └── test_organizer.py
├── sample_files/
├── README.md
└── .gitignore
```

## How to Run

First check Python:

```bash
python --version
```

Run preview mode:

```bash
python main.py sample_files
```

Run actual file organization:

```bash
python main.py sample_files --execute
```

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Output

The application creates folders based on file types and generates:

- organizer.log
- organization_report.csv

Both are stored inside the logs folder in the destination.
