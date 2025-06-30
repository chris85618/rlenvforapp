from RLEnvForApp.domain.llmService.ILlmService import ILlmService


class LlmTemplateService(ILlmService):
    system_prompt: str = ""
    llm: ILlmService = None

    def __init__(self, llm: ILlmService = None):
        self.llm = llm
        super().__init__()

    def set_llm(self, llm: ILlmService) -> None:
        self.llm = llm
    
    def set_system_prompt(self, system_prompt: str, *args) -> None:
        self.system_prompt = system_prompt
        self._set_system_prompt(system_prompt, *args)
    
    def get_system_prompt(self) -> str:
        return self.system_prompt

    def _set_system_prompt(self, system_prompt: str, *args):
        pass

    def get_response(self, system_prompt: str=None, **kwargs) -> str:
        if system_prompt is None:
            system_prompt = self.system_prompt
        prompt = system_prompt.format(**kwargs)
        for _ in range(3):
            response = self.llm.get_response(prompt)
            if response is not None:
                break
        return response

    def get_structured_response(self, system_prompt: str=None, **kwargs):
        if system_prompt is None:
            system_prompt = self.system_prompt
        prompt = system_prompt.format(**kwargs)
        for _ in range(3):
            response = self.llm.get_structured_response(prompt)
            if response is not None:
                break
        return response
