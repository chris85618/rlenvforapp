from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.llmService.LlmTemplateService import LlmTemplateService


llm_service_instance:LlmTemplateService = LlmTemplateService()
llm_service:ILlmService = llm_service_instance
