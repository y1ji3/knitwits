"""
Management command: import_pos_sales
-------------------------------------
Usage:
    python manage.py import_pos_sales path/to/file.jsonl
    python manage.py import_pos_sales path/to/file.json --clear

Options:
    --clear     Delete all existing POSSalesByProductVariant rows before importing.
"""

from django.core.management.base import BaseCommand, CommandError

from yourapp.models import POSSalesByProductVariant  # ← update 'yourapp' to your app name


class Command(BaseCommand):
    help = "Import POS sales data from a JSON or JSONL file into POSSalesByProductVariant."

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to the .json or .jsonl file to import.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            default=False,
            help="Clear all existing records before importing.",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        clear = options["clear"]

        self.stdout.write(f"Importing from: {file_path}")
        if clear:
            self.stdout.write(self.style.WARNING("--clear flag set: existing records will be deleted."))

        try:
            result = POSSalesByProductVariant.import_from_file(file_path, clear_existing=clear)
        except FileNotFoundError:
            raise CommandError(f"File not found: {file_path}")
        except Exception as exc:
            raise CommandError(f"Import failed: {exc}")

        self.stdout.write(self.style.SUCCESS(f"✔ Created: {result['created']}"))

        if result["skipped"]:
            self.stdout.write(self.style.WARNING(f"⚠ Skipped: {result['skipped']}"))
            for err in result["errors"]:
                self.stdout.write(f"  Line {err['line']}: {err['error']} — {err['data']}")
        else:
            self.stdout.write("No rows skipped.")
