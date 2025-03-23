# from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from dependency_injector.wiring import Provide
from RLEnvForApp.domain.targetPage.FormInputValue import FormInputValue
from RLEnvForApp.domain.targetPage.Dom import Dom
from RLEnvForApp.adapter.llmService.groq import Groq


class FormInputValueList:
    # form_xpath = None
    # page_dom = None
    form_input_value_list: list[FormInputValue] = []
    index: int = 0

    def __init__(self, form_xpath, page_dom):
        # self.input_generator = Provide[EnvironmentDIContainers.llmService]
        self.input_generator = Groq()
        self.form_input_value_list = self._generate_input_values(form_xpath, page_dom)
        self.index = 0
        # self.page_dom = page_dom

    def get(self) -> FormInputValue:
        if self.is_done():
            raise IndexError("No more items in the list.")
        return self.form_input_value_list[self.index]

    def next(self):
        self.index += 1
    
    def is_done(self) -> bool:
        return self.index >= len(self.form_input_value_list)

    def _generate_input_values(self, form_xpath: str, page_dom: Dom) -> list[FormInputValue]:
        # Get form elements
        form_elements = page_dom.getByXpath(form_xpath).tostring()
        # Get input values
        input_values = self.input_generator.get_input_value_list(form_elements, form_xpath=form_xpath)
        return input_values
