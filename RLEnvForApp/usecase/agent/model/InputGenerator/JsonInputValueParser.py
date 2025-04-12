import json
from RLEnvForApp.usecase.agent.model.InputGenerator.IInputValueParser import IInputValueParser

class JsonInputValueParser(IInputValueParser):
    def parse(self, input_str: str) -> list:
        try:
            return json.loads(input_str)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
