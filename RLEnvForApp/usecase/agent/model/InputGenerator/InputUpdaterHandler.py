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

    def get_response(self, dom, form_xpath:str):
        response = self.llm_service.get_response(dom=dom, form_xpath=form_xpath)
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

    def get_input_value_list(self, dom, origin_input_values, form_xpath) -> list[FormInputValue]:
        # TODO: verify the result?
        result:list[FormInputValue] = []
        input_value_list_str = self.get_response(dom, input_values=origin_input_values, form_xpath=form_xpath)
        for input_value_dict in self.input_value_parser.parse(input_value_list_str):
            form_input_value_list = FormInputValue(page_dom=dom, form_xpath=form_xpath)
            for xpath, input_value in input_value_dict.items():
                formatted_xpath = XPathFormatter.format(xpath)
                input_value = InputValue(xpath=formatted_xpath, value=input_value["input_value"], action=input_value["action_number"])
                form_input_value_list.append(input_value)
            result.append(form_input_value_list)
            return result
        raise
