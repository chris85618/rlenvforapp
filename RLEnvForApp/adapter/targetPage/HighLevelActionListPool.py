# from RLEnvForApp.usecase.targetPage.HighLevelActionList import HighLevelActionList
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter


class HighLevelActionListPool:
    pool = {}
    # pool:dict[tuple[str, str], HighLevelActionList] = {}

    def add(self, url:str, form_xpath:str, high_level_action_list):
    # def add(self, url:str, form_xpath:str, high_level_action_list:HighLevelActionList):
        self.pool[self._getIndex(url, form_xpath)] = high_level_action_list

    def get(self, url:str, form_xpath:str):
    # def get(self, url:str, form_xpath:str) -> HighLevelActionList:
        return self.pool.get(self._getIndex(url, form_xpath))

    def _getIndex(self, url:str, form_xpath:str) -> tuple:
        return tuple([url, XPathFormatter.format(form_xpath)])
