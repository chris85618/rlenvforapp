from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.targetPage.InputValue import InputValue
from RLEnvForApp.domain.targetPage.FormInputValueList import FormInputValueList
from RLEnvForApp.usecase.agent.model.InputGenerator.InputValueParser import InputValueParser
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory


class InputGeneratorHandler:
    llm_service = None

    def __init__(self, llm_service: ILlmService):
        self.llm_service = llm_service
        # TODO: https://github.com/meta-llama/llama/issues/484
        self.llm_service.set_system_prompt(SystemPromptFactory.get("get_input_values"), "dom")
        self.input_value_parser = InputValueParser()

    def get_response(self, dom):
        response = self.llm_service.get_response(dom=dom)
        result_list = response.split("```")

        if len(result_list) != 3:
            # TODO: 改成retry
            raise
        
        result = result_list[1]
        if result_list[1].startswith("csv"):
            result = result[3:]

        result = result.strip()
        return result

    def get_input_value_list(self, dom) -> list[FormInputValueList]:
        # TODO: verify the result?
        result:list[FormInputValueList] = []
        input_value_list_str = self.get_response(dom)
        for input_value_dict in self.input_value_parser.parse(input_value_list_str):
            form_input_value_list = FormInputValueList()
            for input_value_pair in input_value_dict.items():
                input_value = InputValue(*input_value_pair)
                form_input_value_list.append(input_value)
            result.append(form_input_value_list)
        return result
