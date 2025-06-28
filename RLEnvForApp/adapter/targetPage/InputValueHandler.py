from RLEnvForApp.adapter.targetPage.HighLevelActionListPool import HighLevelActionListPool
from RLEnvForApp.usecase.targetPage.HighLevelActionList import HighLevelActionList
from RLEnvForApp.domain.targetPage.HighLevelAction import HighLevelAction
from RLEnvForApp.domain.targetPage.Dom import Dom
from RLEnvForApp.usecase.agent.model.InputGenerator.InputGeneratorHandler import InputGeneratorHandler


class InputValueHandler:
    high_level_action_list_pool = HighLevelActionListPool()

    def add(self, url:str, form_xpath:str, page_dom:Dom, field_xpath_list:list[str]):
        if self.high_level_action_list_pool.get(url, form_xpath) is not None:
            # Add if and only if necessary
            return

        # Get form elements
        form_elements = page_dom.getByXpath(form_xpath).tostring()
        # Get input values
        high_level_action_list: HighLevelActionList = InputGeneratorHandler().get_response(form_elements, form_xpath=form_xpath, field_xpath_list=field_xpath_list)
        self.high_level_action_list_pool.add(url, form_xpath, high_level_action_list)

    def insert(self, index:int, url:str, form_xpath:str, high_level_action:HighLevelAction):
        high_level_action_list: HighLevelActionList = self.high_level_action_list_pool.get(url, form_xpath)
        if high_level_action_list is None:
            raise ValueError("HighLevelActionList not found.")
        high_level_action_list.insert(index, high_level_action)

    def get(self, url:str, form_xpath:str) -> HighLevelAction:
        high_level_action_list: HighLevelActionList = self.high_level_action_list_pool.get(url, form_xpath)
        if high_level_action_list.is_done():
            return None
        return high_level_action_list.get()

    def get_and_next(self, url:str, form_xpath:str) -> HighLevelAction:
        result = None
        high_level_action_list: HighLevelActionList = self.high_level_action_list_pool.get(url, form_xpath)
        if high_level_action_list is not None:
            if high_level_action_list.is_done() == False:
                result = high_level_action_list.get()
            if high_level_action_list.is_done() == False:
                high_level_action_list.next()
        return result

    def next(self, url:str, form_xpath:str):
        self.get_and_next(url, form_xpath)

    def is_exist(self, url:str, form_xpath:str) -> bool:
        high_level_action_list: HighLevelActionList = self.high_level_action_list_pool.get(url, form_xpath)
        return high_level_action_list is not None

    def is_done(self, url:str, form_xpath:str) -> bool:
        high_level_action_list: HighLevelActionList = self.high_level_action_list_pool.get(url, form_xpath)
        return high_level_action_list.is_done()

    def is_first(self, url:str, form_xpath:str) -> int:
        high_level_action_list: HighLevelActionList = self.high_level_action_list_pool.get(url, form_xpath)
        if high_level_action_list is None:
            raise ValueError("HighLevelActionList not found.")
        return high_level_action_list.is_first()

    def getHighLevelActionList(self, url:str, form_xpath:str) -> HighLevelActionList:
        highLevelActionList: HighLevelActionList = self.high_level_action_list_pool.get(url, form_xpath)
        # if highLevelActionList is None:
        #     raise ValueError("HighLevelActionList not found.")
        return highLevelActionList
