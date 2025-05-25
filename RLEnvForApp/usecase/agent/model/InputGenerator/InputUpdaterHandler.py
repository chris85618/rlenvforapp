from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.LlmTemplateService import LlmTemplateService
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter
from RLEnvForApp.usecase.targetPage.HighLevelActionList import HighLevelActionList


class InputUpdaterHandler:
    llm_service = None

    def __init__(self, llm_service: ILlmService):
        self.llm_service = LlmTemplateService()
        self.llm_service.set_llm(llm_service)
        self.llm_service.set_system_prompt(SystemPromptFactory.get("update_input_values"), "dom", "input_values", "form_xpath", "lacked_field_xpath")

    def get_response(self, dom:str, input_values:str, form_xpath:str, lacked_field_xpath:str) -> str:
        formatted_form_xpath = XPathFormatter.format(form_xpath)
        formatted_lacked_field_xpath = XPathFormatter.format(lacked_field_xpath)
        test_combination_output_response = self.llm_service.get_structured_response(dom=dom, input_values=input_values, form_xpath=formatted_form_xpath, lacked_field_xpath=formatted_lacked_field_xpath)
        high_level_action_list = HighLevelActionList.fromTestCombinationOutputResponse(test_combination_output_response, page_dom=dom, form_xpath=formatted_form_xpath)
        return high_level_action_list
