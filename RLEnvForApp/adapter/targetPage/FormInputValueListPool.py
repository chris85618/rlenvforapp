from RLEnvForApp.adapter.targetPage.FormInputValueList import FormInputValueList
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter


class FormInputValueListPool:
    pool:dict[tuple[str, str], FormInputValueList] = {}

    def add(self, url:str, form_xpath:str, input_value:FormInputValueList):
        self.pool[self._getIndex(url, form_xpath)] = input_value

    def get(self, url:str, form_xpath:str) -> FormInputValueList:
        return self.pool.get(self._getIndex(url, form_xpath))

    def _getIndex(self, url:str, form_xpath:str) -> tuple:
        return tuple([url, XPathFormatter.format(form_xpath)])
