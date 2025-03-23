import csv
import io


class InputValueParser:
    def parse(self, csv_str: str) -> list:
        csv_file = io.StringIO(csv_str)
        reader = csv.DictReader(csv_file)
        return reader
