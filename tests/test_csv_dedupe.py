import csv
import tempfile
import unittest
from pathlib import Path

from examples.csv_dedupe import deduplicate, run


class CsvDedupeTest(unittest.TestCase):
    def test_first_and_last_are_stable(self):
        rows = [
            {"id": "1", "value": "old"},
            {"id": "2", "value": "only"},
            {"id": "1", "value": "new"},
        ]
        self.assertEqual([row["value"] for row in deduplicate(rows, ["id"])], ["old", "only"])
        self.assertEqual(
            [row["value"] for row in deduplicate(rows, ["id"], "last")],
            ["only", "new"],
        )

    def test_csv_round_trip_and_count(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            destination = Path(directory) / "output.csv"
            source.write_text("email,name\na@example.com,A\na@example.com,B\n", encoding="utf-8")
            self.assertEqual(
                run(source, destination, ["email"]),
                {"input_rows": 2, "output_rows": 1},
            )
            with destination.open(newline="", encoding="utf-8") as handle:
                self.assertEqual(list(csv.DictReader(handle)), [{"email": "a@example.com", "name": "A"}])

    def test_unknown_key_fails_clearly(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            source.write_text("id\n1\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown key columns"):
                run(source, Path(directory) / "output.csv", ["missing"])


if __name__ == "__main__":
    unittest.main()

