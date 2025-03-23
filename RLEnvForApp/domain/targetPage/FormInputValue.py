from RLEnvForApp.domain.targetPage.InputValue import InputValue


class FormInputValue:
    input_value_dict: {str, InputValue} = {}
    page_dom:str=""

    def __init__(self, *input_value_list: list[InputValue], page_dom: str = "", form_xpath: str = ""):
        for input_value in input_value_list:
            xpath = input_value.getXpath()
            self.input_value_dict[xpath] = input_value
        self.page_dom = page_dom
        self.form_xpath = form_xpath

    def append(self, input_value: InputValue):
        xpath = input_value.getXpath()
        self.input_value_dict[xpath] = input_value

    def update(self, new_page_dom: str):
        self.page_dom = new_page_dom
        # TODO: Additional update logic can be added here
        

    def getInputValueList(self) -> list[InputValue]:
        return self.input_value_dict.values()
    
    def getInputValueByIndex(self, index) -> InputValue:
        return self.input_value_dict.values()[index]
    
    def getInputValueByXpath(self, xpath:str) -> InputValue:
        return self.input_value_dict.get(xpath)
    
    def getInputValueDict(self) -> dict:
        return self.input_value_dict
    
    def getInputValueItems(self) -> dict:
        return self.input_value_dict.items()
