from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.targetPage.InputValue import InputValue
from RLEnvForApp.domain.targetPage.FormInputValue import FormInputValue
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.LlmTemplateService import LlmTemplateService
from RLEnvForApp.domain.llmService.TestCombinationOutputResponse import TestCombinationOutputResponse
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter
from RLEnvForApp.usecase.agent.model.InputGenerator.IInputValueParser import IInputValueParser
from RLEnvForApp.usecase.agent.model.InputGenerator.JsonInputValueParser import JsonInputValueParser
from RLEnvForApp.usecase.agent.model.InputGenerator.LlmTestCombinationToFormInputValueListConverter import LlmTestCombinationToFormInputValueListConverter
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
        self.input_value_parser: IInputValueParser = JsonInputValueParser()

    def get_response(self, dom, form_xpath:str):
        formatted_form_xpath = XPathFormatter.format(form_xpath)
        test_combination_output_response:TestCombinationOutputResponse = self.llm_service.get_structured_response(dom=dom, form_xpath=formatted_form_xpath)
        return test_combination_output_response

    def get_input_value_list(self, dom, form_xpath) -> list[FormInputValue]:
        # TODO: verify the result?
        formatted_form_xpath = XPathFormatter.format(form_xpath)
        result:list[FormInputValue] = []
        input_value_list_str = self.get_response(dom, form_xpath=formatted_form_xpath)
        for input_value_dict in self.input_value_parser.parse(input_value_list_str):
            form_input_value_list = FormInputValue(page_dom=dom, form_xpath=formatted_form_xpath)
            for xpath, input_value in input_value_dict.items():
                formatted_xpath = XPathFormatter.format(xpath)
                input_value = InputValue(xpath=formatted_xpath, value=input_value["input_value"], action=input_value["action_number"])
                form_input_value_list.append(input_value)
            result.append(form_input_value_list)
        return result
