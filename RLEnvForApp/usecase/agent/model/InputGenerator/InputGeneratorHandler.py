import os
import json
import csv
import re
from typing import Match
from typing import Optional
from datetime import datetime
from langchain.output_parsers import PydanticOutputParser
from markdown_it import MarkdownIt

from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.LlmTemplateService import LlmTemplateService
from RLEnvForApp.domain.llmService.TestCombinationOutputResponse import TestCombinationOutputResponse
from RLEnvForApp.domain.targetPage.HighLevelAction import HighLevelAction
from RLEnvForApp.domain.targetPage.builder.AppEventBuilder import AppEventBuilder
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter
from RLEnvForApp.usecase.agent.model.InputGenerator.PageDomExtractor import PageDomExtractor
from RLEnvForApp.usecase.targetPage.HighLevelActionList import HighLevelActionList
from RLEnvForApp.adapter.llmService.Gemini import Gemini

DATE = datetime.now().strftime('%Y%m%d_%H%M%S')
DIRPATH = f"htmlSet/{DATE}"
PAGE_INFO_PATH = f"{DIRPATH}/PageDomInfo.json"
DESIGN_DOC_PATH = f"{DIRPATH}/{{xpath_replaced}}.md"

MAX_INPUT_LENGTH=300
times_record = {}

def expand_repeated_chars(text_with_repeated_chars_abbr: str) -> str:
    pattern = re.compile(r"\(String of (\d+) '(.|\s)' characters\)")
    def expand_match(match: Match[str]) -> str:
        count = int(match.group(1))
        char_to_repeat = match.group(2)
        return char_to_repeat * count
    return pattern.sub(expand_match, text_with_repeated_chars_abbr)

def write_markdown(form_xpath:str, content:str):
    used_xpath = form_xpath.upper().replace("/","_").replace("[","_").replace("]","_")
    try:
        os.makedirs(DIRPATH)
    except FileExistsError:
        pass

    if used_xpath not in times_record:
        times_record[used_xpath] = 1
    else:
        times_record[used_xpath] += 1
    current_times = times_record[used_xpath]

    for current_max_length in range(95, 1, -5):
        try:
            filepath = DESIGN_DOC_PATH.format(xpath_replaced=f"{used_xpath[-1 * current_max_length :]}{current_times}")
            with open(filepath, "w", encoding='utf8') as markdown_file:
                markdown_file.write(content)
            break
        except OSError:
            pass

def parse_markdown_to_HighLevelAction(markdown_text:str, page_dom:str, form_xpath:str) -> HighLevelActionList:
    # Get Last Table
    start_line = None
    end_line = None
    markdownParser = MarkdownIt().enable("table")
    markdown_tokens = markdownParser.parse(markdown_text)
    for token_index in range(len(markdown_tokens)-1, -1, -1):
        token = markdown_tokens[token_index]
        if token.type == 'table_open':
            start_line, end_line = token.map
            break
    if start_line is None or end_line is None:
        raise ValueError("Failed to parse Markdown to HighLevelActionList.")
    table_lines = markdown_text.splitlines()[start_line:end_line]
    # Replace repeated chars abbr. with actual ones.
    table_lines = [expand_repeated_chars(line) for line in table_lines]
    # Convert Markdown Table to HighLevelActionList
    dict_reader = csv.DictReader(table_lines, delimiter="|")
    # skip first row, i.e. the row between the header and data
    appEventBuilder = AppEventBuilder()
    highLevelactionList:list[HighLevelAction] = []
    appEventList = []
    for row in list(dict_reader)[1:]:
        # strip spaces and ignore first empty column
        for k, v in row.items():
            key = k.strip()
            if len(key) == 0:
                continue
            value = v.strip()
            if key == "Test Case":
                if len(value) > 0:
                    # new test case
                    if len(appEventList) > 0:
                        highLevelactionList.append(HighLevelAction(*appEventList, page_dom=page_dom, form_xpath=form_xpath))
                        appEventList = []
            elif key == "Scenario":
                pass
            elif key == "xpath":
                appEventBuilder.setXpath(value)
            elif key == "action_number":
                appEventBuilder.setCategory(value)
            elif key == "input_value":
                appEventBuilder.setValue(value)
                appEvent = appEventBuilder.build()
                appEventList.append(appEvent)
                appEventBuilder = AppEventBuilder()
            elif key == "Expected Test Result":
                pass
    if len(appEventList) > 0:
        highLevelactionList.append(HighLevelAction(*appEventList, page_dom=page_dom, form_xpath=form_xpath))
        appEventList = []
    return HighLevelActionList(highLevelactionList)
    
class InputGeneratorHandler:
    llm_service = None
    parser = None
    quality_requirements:Optional[str] = None
    tech_stack:Optional[str] = None
    user_personas_and_stories:Optional[str] = None
    business_context:Optional[str] = None
    format_instructions:str = ""

    def __init__(self, llm_service: ILlmService = Gemini()):
        self.llm_service = LlmTemplateService()
        self.llm_service.set_llm(llm_service)
        self.llm_service.set_system_prompt(SystemPromptFactory.get("get_input_values"), "dom", "form_xpath", "field_xpaths", "MAX_INPUT_LENGTH", "quality_requirements", "tech_stack", "user_personas_and_stories", "business_context")
        self.parser = PydanticOutputParser(pydantic_object=TestCombinationOutputResponse)
        self.format_instructions = self.parser.get_format_instructions()

    def get_response(self, dom, form_xpath:str, field_xpath_list:list[str]):
        exception = None
        self.update_web_extracted_data(dom)
        # Form XPath
        formatted_form_xpath = XPathFormatter.format(form_xpath)
        # Field XPath List
        formatted_field_xpath_list = [XPathFormatter.format(field_xpath) for field_xpath in field_xpath_list]
        field_xpaths_str = "\n".join([f"- {field_xpath}" for field_xpath in formatted_field_xpath_list])
        for _ in range(3):
            markdown_doc_str = ""
            try:
                markdown_doc_str = self.llm_service.get_response(SystemPromptFactory.get("get_input_values"), MAX_INPUT_LENGTH=str(MAX_INPUT_LENGTH), dom=dom, form_xpath=field_xpaths_str, field_xpaths=field_xpath_list, quality_requirements=self.quality_requirements, tech_stack=self.tech_stack, user_personas_and_stories=self.user_personas_and_stories, business_context=self.business_context)
                # markdown_doc_str = self.llm_service.get_response(SystemPromptFactory.get("get_input_values") + self.format_instructions.replace("{", "{{").replace("}", "}}"), MAX_INPUT_LENGTH=str(MAX_INPUT_LENGTH), dom=dom, form_xpath=field_xpaths_str, field_xpaths=field_xpath_list, quality_requirements=self.quality_requirements, tech_stack=self.tech_stack, user_personas_and_stories=self.user_personas_and_stories, business_context=self.business_context)
                write_markdown(formatted_form_xpath, markdown_doc_str)
                high_level_action_list:HighLevelActionList = parse_markdown_to_HighLevelAction(markdown_doc_str, dom, form_xpath)
                return high_level_action_list
            except Exception as e:
                exception = e
            print(markdown_doc_str)
        raise exception

    def update_web_extracted_data(self, page_dom):
        if self.quality_requirements is None or self.tech_stack is None or self.user_personas_and_stories is None or self.business_context is None:
            # Update web extracted data
            page_dom_extractor = PageDomExtractor()
            page_dom_info = page_dom_extractor.get_response(page_dom)
            self.business_context = page_dom_extractor.getBusinessContextStr()
            self.user_personas_and_stories = page_dom_extractor.getUserPersonasAndStoriesStr()
            self.tech_stack = page_dom_extractor.getTechnologyStackStr()
            self.quality_requirements = page_dom_extractor.getQualityAttributesStr()
            try:
                os.makedirs(DIRPATH)
            except FileExistsError:
                pass
            with open(PAGE_INFO_PATH, "w", encoding='utf8') as page_info_file:
                page_info_file.write(json.dumps(page_dom_info, indent=4, ensure_ascii=False))
