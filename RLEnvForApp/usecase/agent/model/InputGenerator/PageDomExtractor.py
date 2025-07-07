import json

from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.LlmTemplateService import LlmTemplateService
from RLEnvForApp.domain.llmService.WebExtractedInfo import WebExtractedInfo
from RLEnvForApp.adapter.llmService.Gemini import Gemini

class PageDomExtractor:
    llm_service = None
    llm_service_with_structured_output = None
    business_context:dict = None
    user_personas_and_storiest:dict = None
    tech_stack:list = None
    quality_requirements:list = None

    def __init__(self, llm_service: ILlmService = Gemini(structure_output_format=WebExtractedInfo)):
        self.llm_service = LlmTemplateService()
        self.llm_service.set_llm(llm_service)
        self.llm_service.set_system_prompt(SystemPromptFactory.get("extract_web_info"), "page_dom")

    @staticmethod
    def extract_last_json_block(text):
        lines = text.splitlines()
        blocks = []
        in_block = False
        current_block = []

        for line in lines:
            if line.startswith('{') and not in_block:
                # 開始新的 JSON 區塊
                in_block = True
                current_block = [line]
            elif in_block:
                current_block.append(line)
                if line.startswith('}'):
                    # 區塊結束，存起來
                    blocks.append('\n'.join(current_block))
                    in_block = False

        # 從最後一個區塊開始，嘗試解析
        for block in reversed(blocks):
            try:
                return json.loads(block)
            except json.JSONDecodeError:
                continue

        return None  # 沒有合法 JSON

    def get_response(self, page_dom) -> dict:
        result_json:dict = {}
        for _ in range (3):
            web_extracted_info:str = self.llm_service.get_response(page_dom=page_dom)
            result_json = PageDomExtractor.extract_last_json_block(web_extracted_info)
            if result_json is not None:
                break
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
        return self.user_personas_and_stories
    
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

