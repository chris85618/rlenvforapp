from RLEnvForApp.domain.targetPage.FormInputValue import FormInputValue
from RLEnvForApp.domain.llmService.TestCombinationOutputResponse import TestCombinationOutputResponse


class FormInputValueList:
    # form_xpath = None
    # page_dom = None
    form_input_value_list: list[FormInputValue] = []
    index: int = 0

    def __init__(self, form_input_value_list):
        self.form_input_value_list = form_input_value_list
        self.index = 0
        # self.page_dom = page_dom
    
    @classmethod
    def fromTestCombinationOutputResponse(cls, test_combination_output_response: TestCombinationOutputResponse, page_dom: str = "", form_xpath: str = ""):
        form_input_value_list = []
        # Get input values
        for test_combination in test_combination_output_response.test_combination_list:
            form_input_value = FormInputValue.fromFormOutputResponse(test_combination, page_dom=page_dom, form_xpath=form_xpath)
            form_input_value_list.append(form_input_value)
        result = cls(form_input_value_list)
        return result

    def get(self) -> FormInputValue:
        if self.is_done():
            raise IndexError("No more items in the list.")
        return self.form_input_value_list[self.index]

    def next(self):
        self.index += 1
    
    def is_done(self) -> bool:
        return self.index >= len(self.form_input_value_list)
