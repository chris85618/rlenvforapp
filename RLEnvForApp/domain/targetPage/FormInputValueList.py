from RLEnvForApp.domain.targetPage.InputValue import InputValue


class FormInputValueList:
    input_value_dict: {str, InputValue} = {}

    def __init__(self, *input_value_list:[InputValue]):
        for input_value in input_value_list:
            xpath = input_value.getXpath()
            self.input_value_dict[xpath] = input_value

    def append(self, input_value: InputValue):
        xpath = input_value.getXpath()
        self.input_value_dict[xpath] = input_value
    
    def getInputValueList(self) -> [InputValue]:
        return self.input_value_dict.values()
    
    def getInputValueByIndex(self, index) -> InputValue:
        return self.input_value_dict.values()[index]
    
    def getInputValueByXpath(self, xpath:str) -> InputValue:
        return self.input_value_dict.get(xpath)
    
    def getInputValueItems(self) -> dict:
        return self.input_value_dict
