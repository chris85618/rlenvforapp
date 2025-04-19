from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.targetPage.InputValue import InputValue
from RLEnvForApp.domain.targetPage.FormInputValue import FormInputValue
from RLEnvForApp.usecase.agent.model.InputGenerator.IInputValueParser import IInputValueParser
from RLEnvForApp.usecase.agent.model.InputGenerator.JsonInputValueParser import JsonInputValueParser
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.LlmTemplateService import LlmTemplateService
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter


class InputUpdaterHandler:
    llm_service = None

    def __init__(self, llm_service: ILlmService):
        self.llm_service = LlmTemplateService()
        self.llm_service.set_llm(llm_service)
        # TODO: https://github.com/meta-llama/llama/issues/484
        self.llm_service.set_system_prompt(SystemPromptFactory.get("update_input_values"), "dom", "input_values", "form_xpath")
        self.input_value_parser: IInputValueParser = JsonInputValueParser()

    def get_response(self, dom:str, input_values:str, form_xpath:str):
        response = self.llm_service.get_response(dom=dom, input_values=input_values, form_xpath=form_xpath)
        result_list = response.split("```")

        if len(result_list) < 3:
            # TODO: 改成retry
            raise
        
        for result in reversed(result_list):
            format_str = "json"
            if result.startswith(format_str):
                result = result[len(format_str):]
                result = result.strip()
                return result
        # TODO: 改成retry
        raise

    def get_input_value_list(self, dom, input_values, form_xpath) -> list[FormInputValue]:
        # TODO: verify the result?
        result:list[FormInputValue] = []
        input_value_list_str = self.get_response(dom=dom, input_values=input_values, form_xpath=form_xpath)
        for input_value_dict in self.input_value_parser.parse(input_value_list_str):
            formatted_xpath = XPathFormatter.format(input_value_dict["xpath"])
            input_value = InputValue(xpath=formatted_xpath, value=input_value_dict["input_value"], action=input_value_dict["action_number"])
            form_input_value_list = FormInputValue(input_value, page_dom=dom, form_xpath=form_xpath)
            result.append(form_input_value_list)
            return result
        raise
