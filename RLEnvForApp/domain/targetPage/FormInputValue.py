from RLEnvForApp.domain.targetPage.InputValue import InputValue
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter
from RLEnvForApp.domain.llmService.FormOutputResponse import FormOutputResponse


class FormInputValue:
    input_value_dict: {str, InputValue} = {}
    page_dom:str=""

    def __init__(self, *input_value_list: list[InputValue], page_dom: str = "", form_xpath: str = ""):
        for input_value in input_value_list:
            xpath = input_value.getXpath()
            formatted_xpath = XPathFormatter.format(xpath)
            self.input_value_dict[formatted_xpath] = input_value
        self.page_dom = page_dom
        self.form_xpath = form_xpath
    
    @classmethod
    def fromFormOutputResponse(cls, form_output_response: FormOutputResponse, page_dom: str = "", form_xpath: str = ""):
        result = cls(page_dom=page_dom, form_xpath=form_xpath)
        for test_field_output_response in form_output_response.test_combination_list:
            input_value = InputValue.fromTestFieldOutputResponse(test_field_output_response)
            result.append(input_value)
        return result

    def append(self, input_value: InputValue):
        xpath = input_value.getXpath()
        formatted_xpath = XPathFormatter.format(xpath)
        self.input_value_dict[formatted_xpath] = input_value

    def update(self, new_page_dom: str, form_input_value_dict: dict[str, InputValue]):
        # Update the page DOM if it has changed
        self.page_dom = new_page_dom
        # Update the input value dictionary with new values
        for xpath, input_value in form_input_value_dict.items():
            formatted_xpath = XPathFormatter.format(xpath)
            self.input_value_dict[formatted_xpath] = input_value
        

    def getInputValueList(self) -> list[InputValue]:
        return self.input_value_dict.values()
    
    def getInputValueByIndex(self, index) -> InputValue:
        return self.input_value_dict.values()[index]
    
    def getInputValueByXpath(self, xpath:str) -> InputValue:
        formatted_xpath = XPathFormatter.format(xpath)
        return self.input_value_dict.get(formatted_xpath)
    
    def getInputValueDict(self) -> dict:
        return self.input_value_dict
    
    def getInputValueItems(self) -> dict:
        return self.input_value_dict.items()
    
    def toString(self) -> str:
        result = ""
        for xpath, input_value in self.input_value_dict.items():
            value = input_value.getValue()
            action = input_value.getAction()
            result += f"xpath: {xpath}, input_value: {value}, action_number: {action}\n"
        return result
