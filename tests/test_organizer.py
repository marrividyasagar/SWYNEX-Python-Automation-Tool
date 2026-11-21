
import tempfile
import unittest
from pathlib import Path

from file_organizer.organizer import FileOrganizer


class TestFileOrganizer(unittest.TestCase):

    def setUp(self):

        self.temp = tempfile.TemporaryDirectory()

        self.source = Path(self.temp.name) / "input"

        self.source.mkdir()

        self.organizer = FileOrganizer(
            self.source
        )

    def tearDown(self):

        self.temp.cleanup()

    def test_document_category(self):

        result = self.organizer.get_category(
            Path("report.pdf")
        )

        self.assertEqual(result, "Documents")

    def test_image_category(self):

        result = self.organizer.get_category(
            Path("photo.jpg")
        )

        self.assertEqual(result, "Images")

    def test_unknown_category(self):

        result = self.organizer.get_category(
            Path("file.xyz")
        )

        self.assertEqual(result, "Other")

    def test_preview_does_not_move_files(self):

        file = self.source / "report.pdf"

        file.write_text("test")

        self.organizer.organize_files()

        self.assertTrue(file.exists())

    def test_execute_moves_file(self):

        file = self.source / "report.pdf"

        file.write_text("test")

        self.organizer.organize_files(
            execute=True
        )

        destination = (
            self.source / "Documents" / "report.pdf"
        )

        self.assertTrue(destination.exists())

    def test_duplicate_file_name(self):

        folder = self.source / "Documents"

        folder.mkdir()

        (folder / "report.pdf").write_text("old")

        (self.source / "report.pdf").write_text("new")

        self.organizer.organize_files(
            execute=True
        )

        duplicate = folder / "report_1.pdf"

        self.assertTrue(duplicate.exists())

    def test_missing_folder(self):

        missing = FileOrganizer(
            self.source / "missing"
        )

        with self.assertRaises(FileNotFoundError):

            missing.organize_files()


if __name__ == "__main__":

    unittest.main()
