from RLEnvForApp.adapter.targetPage.FormInputValueListPool import FormInputValueListPool
from RLEnvForApp.usecase.targetPage.FormInputValueList import FormInputValueList
from RLEnvForApp.domain.targetPage.HighLevelAction import HighLevelAction
from RLEnvForApp.domain.targetPage.Dom import Dom
from RLEnvForApp.usecase.agent.model.InputGenerator.InputGeneratorHandler import InputGeneratorHandler


class InputValueHandler:
    input_value_pool = FormInputValueListPool()

    def add(self, url:str, form_xpath:str, page_dom:Dom):
        if self.input_value_pool.get(url, form_xpath) is not None:
            # Add if and only if necessary
            return

        # Get form elements
        form_elements = page_dom.getByXpath(form_xpath).tostring()
        # Get input values
        form_input_value_list: FormInputValueList = InputGeneratorHandler().get_response(form_elements, form_xpath=form_xpath)
        self.input_value_pool.add(url, form_xpath, form_input_value_list)
    
    def insert(self, index:int, url:str, form_xpath:str, high_level_action:HighLevelAction):
        form_input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath)
        if form_input_value_list is None:
            raise ValueError("FormInputValueList not found.")
        form_input_value_list.insert(index, high_level_action)

    def get(self, url:str, form_xpath:str) -> HighLevelAction:
        input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath)
        if input_value_list.is_done():
            return None
        return input_value_list.get()

    def get_and_next(self, url:str, form_xpath:str) -> HighLevelAction:
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

    def is_exist(self, url:str, form_xpath:str) -> bool:
        input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath)
        return input_value_list is not None
    
    def is_done(self, url:str, form_xpath:str) -> bool:
        form_input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath)
        return form_input_value_list.is_done()

    def is_first(self, url:str, form_xpath:str) -> int:
        input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath)
        if input_value_list is None:
            raise ValueError("FormInputValueList not found.")
        return input_value_list.is_first()

    def getFormInputValueList(self, url:str, form_xpath:str) -> FormInputValueList:
        form_input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath)
        # if form_input_value_list is None:
        #     raise ValueError("FormInputValueList not found.")
        return form_input_value_list
