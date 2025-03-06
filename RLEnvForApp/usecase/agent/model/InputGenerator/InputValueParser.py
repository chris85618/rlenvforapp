import csv
import io


class InputValueParser:
    def parse(self, csv: str) -> list:
        csv_file = io.StringIO(csv)
        reader = csv.DictReader(csv_file)
        return reader
