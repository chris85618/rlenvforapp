from RLEnvForApp.domain.targetPage.Dom import Dom
from RLEnvForApp.domain.llmService.TestFieldOutputResponse import TestFieldOutputResponse


class InputValue:
    action:int = None
    xpath:str = ""
    value:str = ""

    def __init__(self, xpath:str, value:str, action=None):
        self.xpath = xpath
        self.value = value
        self.action = action

    @classmethod
    def fromTestFieldOutputResponse(cls, test_field_output_response: TestFieldOutputResponse):
        return cls(
            xpath=test_field_output_response.xpath,
            action=test_field_output_response.action_number,
            value=test_field_output_response.input_value,
        )
    
    def getXpath(self):
        return self.xpath
    
    def getValue(self):
        return self.value
    
    def getAction(self):
        return self.action
