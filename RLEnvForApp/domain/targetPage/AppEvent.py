from RLEnvForApp.domain.llmService.TestFieldOutputResponse import TestFieldOutputResponse
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter


class AppEvent:
    def __init__(self, xpath: str, value: str, category: str):
        self._xpath = str(XPathFormatter.format(xpath))
        self._value = value
        self._category = category

    @classmethod
    def fromTestFieldOutputResponse(cls, test_field_output_response: TestFieldOutputResponse):
        return cls(
            xpath=test_field_output_response.xpath,
            category=test_field_output_response.action_number,
            value=test_field_output_response.input_value,
        )

    def getXpath(self):
        return self._xpath

    def getValue(self):
        return self._value

    def getCategory(self):
        return self._category
