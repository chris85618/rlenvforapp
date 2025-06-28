from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.LlmTemplateService import LlmTemplateService
from RLEnvForApp.domain.llmService.TestCombinationOutputResponse import TestCombinationOutputResponse
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter
from RLEnvForApp.usecase.targetPage.HighLevelActionList import HighLevelActionList
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from dependency_injector.wiring import Provide

class InputGeneratorHandler:
    llm_service = None
    llm_service_with_structured_output = None

    def __init__(self, llm_service: ILlmService = Provide[EnvironmentDIContainers.llmService]):
        self.llm_service = LlmTemplateService()
        self.llm_service.set_llm(llm_service)
        self.llm_service.set_system_prompt(SystemPromptFactory.get("get_input_values"), "dom", "form_xpath")

    def get_response(self, dom, form_xpath:str):
        formatted_form_xpath = XPathFormatter.format(form_xpath)
        for _ in range(10):
            test_combination_output_response:TestCombinationOutputResponse = self.llm_service.get_structured_response(dom=dom, form_xpath=formatted_form_xpath)
            if test_combination_output_response is not None:
                break
        high_level_action_list = HighLevelActionList.fromTestCombinationOutputResponse(test_combination_output_response, page_dom=dom, form_xpath=formatted_form_xpath)
        return high_level_action_list
