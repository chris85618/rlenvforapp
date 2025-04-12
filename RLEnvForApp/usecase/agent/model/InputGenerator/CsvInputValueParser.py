import csv
import io
from RLEnvForApp.usecase.agent.model.InputGenerator.IInputValueParser import IInputValueParser

class CsvInputValueParser(IInputValueParser):
    def parse(self, input_str: str) -> list:
        csv_file = io.StringIO(input_str)
        reader = csv.DictReader(csv_file)
        return reader
