from RLEnvForApp.adapter.targetPage.FormInputValueListPool import FormInputValueListPool
from RLEnvForApp.adapter.targetPage.FormInputValueList import FormInputValueList
from RLEnvForApp.domain.targetPage.FormInputValue import FormInputValue
from RLEnvForApp.domain.targetPage.Dom import Dom


class InputValueHandler:
    input_value_pool = FormInputValueListPool()

    def add(self, url:str, xpath:str, page_dom:Dom):
        if self.input_value_pool.get(url, xpath) is not None:
            # Add if and only if necessary
            return
        form_input_value_list: FormInputValueList = FormInputValueList(xpath, page_dom)
        self.input_value_pool.add(url, xpath, form_input_value_list)

    def get(self, url:str, form_xpath:str) -> FormInputValue:
        input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath)
        if input_value_list.is_done():
            return None
        return input_value_list.get()

    def get_and_next(self, url:str, form_xpath:str) -> FormInputValue:
        form_input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath)
        if form_input_value_list is not None:
            if form_input_value_list.is_done() == False:
                form_input_value_list.next()
            if form_input_value_list.is_done() == False:
                return form_input_value_list.get()
        return None

    def next(self, url:str, form_xpath:str):
        self.get_and_next(url, form_xpath)
