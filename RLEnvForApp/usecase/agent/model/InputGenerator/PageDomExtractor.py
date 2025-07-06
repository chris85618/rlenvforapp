import json

from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.LlmTemplateService import LlmTemplateService
from RLEnvForApp.domain.llmService.WebExtractedInfo import WebExtractedInfo
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from dependency_injector.wiring import Provide

class PageDomExtractor:
    llm_service = None
    llm_service_with_structured_output = None
    business_context:dict = None
    user_personas_and_storiest:dict = None
    tech_stack:list = None
    quality_requirements:list = None

    def __init__(self, llm_service: ILlmService = Provide[EnvironmentDIContainers.llmService]):
        self.llm_service = LlmTemplateService()
        self.llm_service.set_llm(llm_service)
        self.llm_service.set_system_prompt(SystemPromptFactory.get("extract_web_info"), "page_dom")

    def get_response(self, page_dom) -> WebExtractedInfo:
        web_extracted_info:WebExtractedInfo = self.llm_service.get_structured_response(page_dom=page_dom)
        result_json:dict = web_extracted_info.model_dump()
        # Business Context
        self.business_context = {
                                    "applicationType": result_json["applicationType"],
                                    "coreBusinessGoal": result_json["coreBusinessGoal"],
                                    "supportingFunctionality": result_json["supportingFunctionality"],
                                }
        # Target Audience Personas
        self.user_personas_and_stories = result_json["targetAudiencePersonas"]
        # Technology Stack
        self.tech_stack = result_json["technologyStack"]
        # Quality Attributes
        self.quality_requirements = result_json["inferredQualityAttributes"]
        return result_json
    
    def getBusinessContext(self) -> dict:
        return self.business_context
    
    def getBusinessContextStr(self) -> str:
        return json.dumps(self.getBusinessContext(), indent=4, ensure_ascii=False)
    
    def getUserPersonasAndStories(self) -> dict:
        return self.ser_personas_and_stories
    
    def getUserPersonasAndStoriesStr(self) -> str:
        return json.dumps(self.getUserPersonasAndStories(), indent=4, ensure_ascii=False)
    
    def getTechnologyStack(self) -> list:
        return self.tech_stack
    
    def getTechnologyStackStr(self) -> str:
        return json.dumps(self.getTechnologyStack(), indent=4, ensure_ascii=False)
    
    def getQualityAttributes(self) -> list:
        return self.quality_requirements
    
    def getQualityAttributesStr(self) -> str:
        return json.dumps(self.getQualityAttributes(), indent=4, ensure_ascii=False)

