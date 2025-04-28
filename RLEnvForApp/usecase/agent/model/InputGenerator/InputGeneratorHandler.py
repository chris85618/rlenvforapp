from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.targetPage.InputValue import InputValue
from RLEnvForApp.domain.targetPage.FormInputValue import FormInputValue
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.LlmTemplateService import LlmTemplateService
from RLEnvForApp.domain.llmService.TestCombinationOutputResponse import TestCombinationOutputResponse
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter
from RLEnvForApp.usecase.agent.model.InputGenerator.IInputValueParser import IInputValueParser
from RLEnvForApp.usecase.targetPage.FormInputValueList import FormInputValueList
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from dependency_injector.wiring import Provide

class InputGeneratorHandler:
    llm_service = None
    llm_service_with_structured_output = None

    def __init__(self, llm_service: ILlmService = Provide[EnvironmentDIContainers.llmService]):
        self.llm_service = LlmTemplateService()
        self.llm_service.set_llm(llm_service)
        # TODO: https://github.com/meta-llama/llama/issues/484
        self.llm_service.set_system_prompt(SystemPromptFactory.get("get_input_values"), "dom")

    def get_response(self, dom, form_xpath:str):
        formatted_form_xpath = XPathFormatter.format(form_xpath)
        test_combination_output_response:TestCombinationOutputResponse = self.llm_service.get_structured_response(dom=dom, form_xpath=formatted_form_xpath)
        return test_combination_output_response

    def get_input_value_list(self, dom, form_xpath) -> list[FormInputValue]:
        # TODO: verify the result?
        formatted_form_xpath = XPathFormatter.format(form_xpath)
        test_combination_output_response = self.get_response(dom, form_xpath=formatted_form_xpath)
        form_input_value_list = FormInputValueList.fromTestCombinationOutputResponse(test_combination_output_response, page_dom=dom, form_xpath=formatted_form_xpath)
        return form_input_value_list
