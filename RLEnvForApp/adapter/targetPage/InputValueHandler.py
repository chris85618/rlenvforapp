from RLEnvForApp.adapter.targetPage.FormInputValueListPool import FormInputValueListPool
from RLEnvForApp.adapter.targetPage.FormInputValueList import FormInputValueList
from RLEnvForApp.domain.targetPage.FormInputValue import FormInputValue
from RLEnvForApp.domain.targetPage.Dom import Dom


class InputValueHandler:
    input_value_pool = FormInputValueListPool()

    def add(self, url:str, xpath:str, page_dom:Dom):
        form_input_value_list: FormInputValueList = FormInputValueList(xpath, page_dom)
        self.input_value_pool.add(url, xpath, form_input_value_list)

    def get(self, url:str, form_xpath:str, field_xpath:str) -> FormInputValue:
        input_value_list: FormInputValueList = self.input_value_pool.get(url, form_xpath, field_xpath)
        if input_value_list.is_done():
            return None
        return input_value_list.get()

    def get_and_next(self, url:str, form_xpath:str, field_xpath:str) -> FormInputValue:
        result: FormInputValueList = self.get(url, form_xpath, field_xpath)
        if result is not None:
            result.next()
        return result

    def next(self, url:str, form_xpath:str, field_xpath:str):
        self.get_and_next(url, form_xpath, field_xpath)
