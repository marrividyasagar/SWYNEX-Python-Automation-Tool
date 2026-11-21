
import csv
import logging
import shutil
from datetime import datetime
from pathlib import Path


# File categories and their extensions
CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Presentations": [".ppt", ".pptx"],
    "Archives": [".zip", ".rar"],
    "Code": [".py", ".html", ".css", ".js"],
}


class FileOrganizer:

    def __init__(self, source, destination=None):
        self.source = Path(source).expanduser().resolve()

        self.destination = (
            Path(destination).expanduser().resolve()
            if destination else self.source
        )

        self.log_dir = self.destination / "logs"
        self.report_path = self.log_dir / "organization_report.csv"

        self.logger = None

    def setup_logging(self):

        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(
            f"swynex_organizer_{id(self)}"
        )

        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        handler = logging.FileHandler(
            self.log_dir / "organizer.log",
            encoding="utf-8"
        )

        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
        )

        self.logger.addHandler(handler)

    def get_category(self, file):

        extension = file.suffix.lower()

        for category, extensions in CATEGORIES.items():

            if extension in extensions:
                return category

        return "Other"

    def get_unique_path(self, path):

        if not path.exists():
            return path

        counter = 1

        while True:

            new_path = path.with_name(
                f"{path.stem}_{counter}{path.suffix}"
            )

            if not new_path.exists():
                return new_path

            counter += 1

    def organize_files(self, execute=False):

        if not self.source.exists():
            raise FileNotFoundError(
                f"Source folder not found: {self.source}"
            )

        if not self.source.is_dir():
            raise NotADirectoryError(
                "Source path must be a folder."
            )

        if (
            self.destination.exists()
            and not self.destination.is_dir()
        ):
            raise NotADirectoryError(
                "Destination path must be a folder."
            )

        self.setup_logging()

        results = []

        for file in sorted(self.source.iterdir()):

            if not file.is_file():
                continue

            # Ignore hidden files such as .gitkeep
            if file.name.startswith("."):
                continue

            category = self.get_category(file)

            target_folder = self.destination / category

            target_path = self.get_unique_path(
                target_folder / file.name
            )

            result = {
                "name": file.name,
                "category": category,
                "target": str(target_path),
                "status": "ready",
                "error": ""
            }

            if execute:

                try:

                    target_folder.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                    target_path = self.get_unique_path(
                        target_folder / file.name
                    )

                    shutil.move(
                        str(file),
                        str(target_path)
                    )

                    result["target"] = str(target_path)

                    self.logger.info(
                        "Moved %s to %s",
                        file.name,
                        target_path
                    )

                except (OSError, shutil.Error) as error:

                    result["status"] = "error"
                    result["error"] = str(error)

                    self.logger.error(
                        "Could not move %s: %s",
                        file.name,
                        error
                    )

            else:

                self.logger.info(
                    "Preview: %s -> %s",
                    file.name,
                    target_path
                )

            results.append(result)

        return results

    def generate_report(self, results):

        self.log_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )

        with open(
            self.report_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            fields = [
                "timestamp",
                "name",
                "category",
                "target",
                "status",
                "error"
            ]

            writer = csv.DictWriter(
                csvfile,
                fieldnames=fields
            )

            writer.writeheader()

            for result in results:

                writer.writerow({
                    "timestamp": timestamp,
                    **result
                })

        return self.report_path
