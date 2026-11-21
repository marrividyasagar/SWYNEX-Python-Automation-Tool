
import argparse
from pathlib import Path

from file_organizer.organizer import FileOrganizer


def main():

    parser = argparse.ArgumentParser(
        description="SWYNEX Python File Organizer"
    )

    parser.add_argument(
        "source",
        nargs="?",
        default="sample_files",
        help="Folder containing files to organize"
    )

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually move the files"
    )

    parser.add_argument(
        "--destination",
        default=None,
        help="Optional destination folder"
    )

    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()

    destination = (
        Path(args.destination).expanduser().resolve()
        if args.destination else source
    )

    try:

        organizer = FileOrganizer(
            source,
            destination
        )

        results = organizer.organize_files(
            execute=args.execute
        )

        report = organizer.generate_report(results)

        print("\n===================================")
        print("       SWYNEX FILE ORGANIZER")
        print("===================================")

        print(
            "Mode:",
            "EXECUTION" if args.execute else "PREVIEW"
        )

        for item in results:

            if item["status"] == "error":
                action = "Skipped"
            elif args.execute:
                action = "Moved"
            else:
                action = "Would move"

            print(
                f'{action}: {item["name"]} '
                f'-> {item["category"]}/'
            )

        print("-----------------------------------")

        print("Total files:", len(results))

        print("Report saved at:", report)

        if not args.execute:

            print(
                "\nPreview completed. "
                "Use --execute to move files."
            )

    except (OSError, ValueError) as error:

        print("Error:", error)


if __name__ == "__main__":
    main()
