from RLEnvForApp.adapter.targetPage.FormInputValueListPool import FormInputValueListPool
from RLEnvForApp.usecase.targetPage.FormInputValueList import FormInputValueList
from RLEnvForApp.domain.targetPage.FormInputValue import FormInputValue
from RLEnvForApp.domain.targetPage.Dom import Dom
from RLEnvForApp.usecase.agent.model.InputGenerator.InputGeneratorHandler import InputGeneratorHandler
from RLEnvForApp.usecase.agent.model.InputGenerator.LlmTestCombinationToFormInputValueListConverter import LlmTestCombinationToFormInputValueListConverter


class InputValueHandler:
    input_value_pool = FormInputValueListPool()

    def add(self, url:str, form_xpath:str, page_dom:Dom):
        if self.input_value_pool.get(url, form_xpath) is not None:
            # Add if and only if necessary
            return

        # Get form elements
        form_elements = page_dom.getByXpath(form_xpath).tostring()
        # Get input values
        form_input_value_list = InputGeneratorHandler().get_response(form_elements, form_xpath=form_xpath)
        self.input_value_pool.add(url, form_xpath, form_input_value_list)

    def get(self, url:str, form_xpath:str) -> FormInputValue:
        input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath)
        if input_value_list.is_done():
            return None
        return input_value_list.get()

    def get_and_next(self, url:str, form_xpath:str) -> FormInputValue:
        result = None
        form_input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath)
        if form_input_value_list is not None:
            if form_input_value_list.is_done() == False:
                result = form_input_value_list.get()
            if form_input_value_list.is_done() == False:
                form_input_value_list.next()
        return result

    def next(self, url:str, form_xpath:str):
        self.get_and_next(url, form_xpath)
