from RLEnvForApp.domain.targetPage.HighLevelAction import HighLevelAction
from RLEnvForApp.domain.llmService.TestCombinationOutputResponse import TestCombinationOutputResponse


class FormInputValueList:
    # form_xpath = None
    # page_dom = None
    high_level_action_list: list[HighLevelAction] = []
    index: int = 0

    def __init__(self, high_level_action_list):
        self.high_level_action_list = high_level_action_list
        self.index = 0
        # self.page_dom = page_dom
    
    @classmethod
    def fromTestCombinationOutputResponse(cls, test_combination_output_response: TestCombinationOutputResponse, page_dom: str = "", form_xpath: str = ""):
        high_level_action_list = []
        # Get input values
        for test_combination in test_combination_output_response.test_combination_list:
            high_level_action = HighLevelAction.fromFormOutputResponse(test_combination, page_dom=page_dom, form_xpath=form_xpath)
            high_level_action_list.append(high_level_action)
        result = cls(high_level_action_list)
        return result

    def get(self) -> HighLevelAction:
        if self.is_done():
            raise IndexError("No more items in the list.")
        return self.high_level_action_list[self.index]

    def next(self):
        self.index += 1
    
    def is_done(self) -> bool:
        return self.index >= len(self.high_level_action_list)
    
    def is_first(self) -> bool:
        return self.index == 0
    
    # TODO: describe side effect
    def insert(self, index:int, high_level_action:HighLevelAction):
        self.high_level_action_list.insert(index, high_level_action)
