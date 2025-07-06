from typing import Optional

from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.LlmTemplateService import LlmTemplateService
from RLEnvForApp.domain.llmService.TestCombinationOutputResponse import TestCombinationOutputResponse
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter
from RLEnvForApp.usecase.agent.model.InputGenerator.PageDomExtractor import PageDomExtractor
from RLEnvForApp.usecase.targetPage.HighLevelActionList import HighLevelActionList
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from dependency_injector.wiring import Provide

class InputGeneratorHandler:
    llm_service = None
    llm_service_with_structured_output = None
    quality_requirements:Optional[str] = None
    tech_stack:Optional[str] = None
    user_personas_and_stories:Optional[str] = None
    business_context:Optional[str] = None

    def __init__(self, llm_service: ILlmService = Provide[EnvironmentDIContainers.llmService]):
        self.llm_service = LlmTemplateService()
        self.llm_service.set_llm(llm_service)
        self.llm_service.set_system_prompt(SystemPromptFactory.get("get_input_values"), "dom", "form_xpath", "field_xpaths")

    def get_response(self, dom, form_xpath:str, field_xpath_list:list[str]):
        self.update_web_extracted_data(dom)
        # Form XPath
        formatted_form_xpath = XPathFormatter.format(form_xpath)
        # Field XPath List
        formatted_field_xpath_list = [XPathFormatter.format(field_xpath) for field_xpath in field_xpath_list]
        field_xpaths_str = "\n".join([f"- {field_xpath}" for field_xpath in formatted_field_xpath_list])
        test_combination_output_response:TestCombinationOutputResponse = self.llm_service.get_structured_response(page_dom=dom, form_xpath=field_xpaths_str, field_xpaths=field_xpath_list, quality_requirements=self.quality_requirements, tech_stack=self.tech_stack, user_personas_and_stories=self.user_personas_and_stories, business_context=self.business_context)
        high_level_action_list = HighLevelActionList.fromTestCombinationOutputResponse(test_combination_output_response, page_dom=dom, form_xpath=formatted_form_xpath)
        return high_level_action_list

    def update_web_extracted_data(self, page_dom):
        if self.quality_requirements is None or self.tech_stack is None or self.user_personas_and_stories is None or self.business_context is None:
            # Update web extracted data
            page_dom_extractor = PageDomExtractor()
            page_dom_extractor.get_response(page_dom)
            self.business_context = page_dom_extractor.getBusinessContextStr()
            self.user_personas_and_stories = page_dom_extractor.getUserPersonasAndStoriesStr()
            self.tech_stack = page_dom_extractor.getTechnologyStackStr()
            self.quality_requirements = page_dom_extractor.getQualityAttributesStr()
