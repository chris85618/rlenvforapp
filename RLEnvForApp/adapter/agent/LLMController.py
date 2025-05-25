import json
import os
import re
import traceback
import time
from io import StringIO
from urllib.parse import urlparse

from typing import Optional

from dependency_injector.wiring import Provide, inject
from lxml import etree

from RLEnvForApp.adapter.controller.ApplicationUnderTestController import ApplicationUnderTestController
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.CodeCoverageCollectorFactory import CodeCoverageCollectorFactory
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.NoCodeCoverageCollector import \
    NoCodeCoverageCollector
from RLEnvForApp.adapter.environment.autOperator.crawler.SeleniumCrawler import SeleniumCrawler
from RLEnvForApp.adapter.llmService.Gemini import Gemini
from RLEnvForApp.adapter.targetPagePort.FileManager import FileManager
from RLEnvForApp.adapter.targetPagePort.factory.TargetPagePortFactory import TargetPagePortFactory
from RLEnvForApp.domain.environment.actionCommand.InitiateToTargetActionCommand import NosuchElementException
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.llmService import LlmServiceContainer
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.targetPage.DirectiveRuleService.FormSubmitCriteriaSingleton import FormSubmitCriteriaSingleton
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import IDirectiveRuleService
from RLEnvForApp.domain.targetPage.Dom import Dom
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.HighLevelAction import HighLevelAction
from RLEnvForApp.domain.environment.actionCommandFactoryService.defaultValue.IDefaultValue import IDefaultValue
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.agent.model.InputGenerator.InputGeneratorHandler import InputGeneratorHandler
from RLEnvForApp.usecase.agent.model.InputGenerator.InputUpdaterHandler import InputUpdaterHandler
from RLEnvForApp.adapter.targetPage.InputValueHandler import InputValueHandler

from RLEnvForApp.usecase.environment.autOperator.AIGUIDEOperator import AIGUIDEOperator
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import EpisodeHandlerDTO
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerInput import GetEpisodeHandlerInput
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerOutput import GetEpisodeHandlerOutput
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerUseCase import GetEpisodeHandlerUseCase
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.environment.executeAction.ExecuteActionInput import ExecuteActionInput
from RLEnvForApp.usecase.environment.executeAction.ExecuteActionOutput import ExecuteActionOutput
from RLEnvForApp.usecase.environment.executeAction.ExecuteActionUseCase import ExecuteActionUseCase
from RLEnvForApp.usecase.environment.resetEnvironment.ResetEnvironmentInput import ResetEnvironmentInput
from RLEnvForApp.usecase.environment.resetEnvironment.ResetEnvironmentOutput import ResetEnvironmentOutput
from RLEnvForApp.usecase.environment.resetEnvironment.ResetEnvironmentUseCase import ResetEnvironmentUseCase
from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository
from RLEnvForApp.usecase.repository.TargetPageRepository import TargetPageRepository
from RLEnvForApp.usecase.targetPage.HighLevelActionList import HighLevelActionList
from RLEnvForApp.usecase.targetPage.create.CreateDirectiveInput import CreateDirectiveInput
from RLEnvForApp.usecase.targetPage.create.CreateDirectiveOutput import CreateDirectiveOutput
from RLEnvForApp.usecase.targetPage.create.CreateDirectiveUseCase import CreateDirectiveUseCase
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageInput import RemoveTargetPageInput
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageOutput import RemoveTargetPageOutput
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageUseCase import RemoveTargetPageUseCase
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.llmService.LlmServiceContainer import llm_service_instance

class LLMController:

    @inject
    def __init__(self,
                 episode_handler_repository: EpisodeHandlerRepository =
                 Provide[EnvironmentDIContainers.episodeHandlerRepository],
                 directive_rule_service: IDirectiveRuleService =
                 Provide[EnvironmentDIContainers.directiveRuleService],
                 repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository],
                 llm_service: ILlmService = Provide[EnvironmentDIContainers.llmService],
                 default_value_fetcher: IDefaultValue = Provide[EnvironmentDIContainers.defaultValueFetcher]):

        self._episode_handler_id = None
        self._form_counts = {}
        self._directive_rule_service = directive_rule_service
        self._episode_handler_repository = episode_handler_repository
        self._repository = repository
        self.__server_name = "keystonejs_with_coverage"
        self.__application_ip = "localhost"
        self.__application_port = 3100
        self.__coverage_server_port = 3100
        self.__code_coverage_type = "statement coverage"

        default_value_fetcher.set_aut_name(self.__server_name)
        self._default_value_fetcher = default_value_fetcher

        self._llm_service = llm_service
        llm_service_instance.set_llm(llm_service)

        self._inputValueHandler = InputValueHandler()

        self._logger = Logger()
        self._logger.info("Init LLM.Env")
        self.__aut_controller = ApplicationUnderTestController(applicationName=self.__server_name,
                                                               serverIP=self.__application_ip,
                                                               port=self.__application_port)
        self.__crawler = SeleniumCrawler("Chrome")
        self.__code_coverage_collector: ICodeCoverageCollector = CodeCoverageCollectorFactory().createCollector(
            server_name=self.__server_name, serverIp=self.__application_ip, serverPort=self.__coverage_server_port)
        # self.__code_coverage_collector: ICodeCoverageCollector = NoCodeCoverageCollector()
        self.__aut_operator = AIGUIDEOperator(
            crawler=self.__crawler, codeCoverageCollector=self.__code_coverage_collector)
        self.__target_page_port = TargetPagePortFactory().createAIGuideTargetPagePort(javaIp="127.0.0.1",
                                                                                      pythonIp="127.0.0.1",
                                                                                      javaPort=2700, pythonPort=2701,
                                                                                      serverName=self.__server_name,
                                                                                      rootUrl=f"http://"
                                                                                              f"{self.__application_ip}:"
                                                                                              f"{self.__application_port}/",
                                                                                      codeCoverageType=
                                                                                      self.__code_coverage_type)
        self.__target_page_port.connect()
        self.__target_form_xpath = ''
        self.__form_counts = {}
        self._target_page_id = ""
        self._episodeIndex = 0
        self.__aut_controller.startAUTServer()

        self.input_generator = InputGeneratorHandler()

    def play(self):
        while True:
            if len(self._repository.findAll()) == 0:
                self.__target_page_port.waitForTargetPage()
            begin_time = time.time_ns()
            self.__aut_controller.resetAUTServer(True)
            self._episodeIndex += 1
            is_legal_directive = False

            try:
                reset_env_use_output = self._reset_environment()
            except NosuchElementException:
                continue

            target_page_url = reset_env_use_output.getTargetPageUrl()
            FormSubmitCriteriaSingleton.getInstance().setFormSubmitCriteria(applicationName=self.__server_name, url=target_page_url, xpath=reset_env_use_output.getFormXPath())
            self._target_page_id = reset_env_use_output.getTargetPageId()
            self._episode_handler_id = reset_env_use_output.getEpisodeHandlerId()
            self.__target_form_xpath = reset_env_use_output.getFormXPath()

            state = self.__aut_operator.getState()

            # Get current app element from crawler
            app_element: AppElement = self.__aut_operator.getFocusedAppElement()
            if app_element is None:
                if len(self.__aut_operator.getAllSelectedAppElements()) == 0:
                    self._remove_target_page()
                break

            state = self.__aut_operator.getState()
            self._inputValueHandler.add(target_page_url, self.__target_form_xpath, Dom(state.getDOM()))
            # Add valid input values if the elements have default values.
            if self._inputValueHandler.is_first(target_page_url, self.__target_form_xpath):
                if self._inputValueHandler.is_done(target_page_url, self.__target_form_xpath) == False:
                    high_level_action:HighLevelAction = self._inputValueHandler.get(target_page_url, self.__target_form_xpath)
                    default_value = self._get_default_value(target_page_url, high_level_action)
                    if default_value is not None:
                        first_index = 0
                        self._inputValueHandler.insert(first_index, target_page_url, self.__target_form_xpath, default_value)

            if self._target_page_id not in self._form_counts:
                self._form_counts[self._target_page_id] = 1

            try:
                self._logger.info(f"Find legal directive, target page id: {self._target_page_id}")
                self._logger.info(f"Number of attempts: {self._form_counts[self._target_page_id]}")
                self.__target_page_port.pushTargetPage(self._target_page_id, self._episode_handler_id, highLevelActionList=self._inputValueHandler.getHighLevelActionList(target_page_url, self.__target_form_xpath))
            except Exception as ex:
                template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
                message = template.format(type(ex).__name__, ex.args)
                self._logger.info(message)
                self._logger.info(f"PUSH ERROR!!! {self.__crawler.getUrl()}")

            end_time = time.time_ns()
            print(f"Total time: {(end_time - begin_time) / 1000000}ms")

    def _check_is_password(self, app_element: AppElement):
        # check if the element is a password field use regex
        if re.search(r'password', app_element.getName(), re.IGNORECASE) or re.search(r'password', app_element.getLabel(),
                                                                                   re.IGNORECASE) or re.search(
                r'password', app_element.getPlaceholder(), re.IGNORECASE):
            return True
        return False

    def _save_target_page_to_html_set(self, episode_handler_id: str, directive_dto: DirectiveDTO):
        file_name = f"{self.__server_name}_{urlparse(directive_dto.getUrl()).path.replace('/', '_')}_{directive_dto.getFormXPath().replace('/', '_')}"
        initial_state_dto: StateDTO = self._get_episode_handler_dto(
            episode_handler_id=episode_handler_id).getStateDTOs()[0]

        interactive_app_element_dictionary = []
        directive_dictionary = {}
        for app_event_dto in directive_dto.getAppEventDTOs():
            directive_dictionary[app_event_dto.getXpath()] = {
                "value": app_event_dto.getValue(), "category": app_event_dto.getCategory()}
        for app_element_dto in initial_state_dto.getSelectedAppElementDTOs():
            interactive_app_element_dictionary.append(app_element_dto.getXpath())
        form_x_path = directive_dto.getFormXPath()
        directive_log_json = json.dumps({"interactive_appElement": interactive_app_element_dictionary,
                                         "appEvent": directive_dictionary, "formXPath": form_x_path})

        # self._updateInputValueWeights(directiveDictionary)

        Logger().info(f"Save html set:\n{file_name}\n{form_x_path}\n{directive_dictionary}")

        file_manager = FileManager()
        file_manager.createFolder("htmlSet", "FAILED_HTML_SET")
        file_manager.createFile(path=os.path.join("htmlSet", "FAILED_HTML_SET"),
                                fileName=file_name + ".html", context=directive_dto.getDom())
        file_manager.createFile(path=os.path.join("htmlSet", "FAILED_HTML_SET"),
                                fileName=file_name + ".json", context=directive_log_json)

    def _create_directive(self, target_page_id: str, episode_handler_id: str, high_level_action_list: HighLevelActionList):
        create_directive_use_case = CreateDirectiveUseCase()
        create_directive_input = CreateDirectiveInput(targetPageId=target_page_id, episodeHandlerId=episode_handler_id, highLevelActionList=high_level_action_list)
        create_directive_output = CreateDirectiveOutput()
        create_directive_use_case.execute(create_directive_input, create_directive_output)
        return create_directive_output.getDirectiveDTO()

    def _get_episode_handler_dto(self, episode_handler_id: str) -> EpisodeHandlerDTO:
        use_case = GetEpisodeHandlerUseCase()
        _input = GetEpisodeHandlerInput(episodeHandlerId=episode_handler_id)
        _output = GetEpisodeHandlerOutput()
        use_case.execute(_input, _output)
        return _output.getEpisodeHandlerDTO()

    def _execute_action(self, app_element: AppElement, target_url: str, form_xpath: str) -> ExecuteActionOutput:
        final_submit = False
        episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
        episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
        states = episode_handler.getAllState()
        xpath = app_element.getXpath()

        # get input values
        high_level_action: HighLevelAction = self._inputValueHandler.get(target_url, form_xpath)
        if high_level_action is None:
            # FInish testing this form
            execute_action_output = ExecuteActionOutput()
            execute_action_output.setIsDone(True)
            return execute_action_output

        execute_action_use_case = ExecuteActionUseCase(self.__aut_operator)
        doc = etree.parse(StringIO(states[-1].getDOM()), etree.HTMLParser())
        # find the submit button by xpath
        app_element_by_xpath = doc.xpath(app_element.getXpath())[0]
        str1 = 'The Form element:\n' + etree.tostring(doc.xpath(self.__target_form_xpath)[0], pretty_print=True, method="html", encoding="unicode") + '\nThe target element:\n' + etree.tostring(app_element_by_xpath, pretty_print=True, method="html", encoding="unicode")
        is_submit_button = False

        prompt = SystemPromptFactory.get("is_submit_button").format(form_info=str1)
        is_submit_button_str = self._llm_service.get_response(prompt).lower()
        if "yes" in is_submit_button_str:
            is_submit_button = True

        # if app_element.getTagName() == "button" or app_element.getTagName() == "a" or (app_element.getTagName() == 'input' and (app_element.getType() == 'submit' or app_element.getType() == "button" or app_element.getType() == 'image')):
        #     is_submit_button = True

        execute_action_output = ExecuteActionOutput()

        if is_submit_button:
            category = 0
            final_submit = True
            app_event = AppEvent("", "", 0)
        else:
            repeat_counter = 0
            app_event: AppEvent = high_level_action.getAppEventByXpath(xpath)
            while app_event is None:
                if repeat_counter >= 3:
                    raise ValueError("Form input value is None for 3 times.")
                repeat_counter += 1
                # Get new state
                state = self.__aut_operator.getState()
                dom = state.getDOM()
                # Update input values
                new_high_level_action_list: HighLevelActionList = InputUpdaterHandler(llm_service=Gemini()).get_response(dom=dom, input_values=high_level_action.toString(), form_xpath=form_xpath, lacked_field_xpath=xpath)
                if new_high_level_action_list.is_done() == False:
                    high_level_action = new_high_level_action_list.get()
                    high_level_action.update(dom, high_level_action.getAppEventDict())
                    app_event: AppEvent = high_level_action.getAppEventByXpath(xpath)
            category = app_event.getCategory()

        execute_action_input = ExecuteActionInput(category, self._episode_handler_id, self.__server_name, target_url,
                                                  app_element.getXpath(), value=app_event.getValue())

        try:
            execute_action_use_case.execute(input=execute_action_input, output=execute_action_output)
            episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
            episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
            state: State = episode_handler.getAllState()[-2]
        except Exception as exception:
            self._logger.exception(f"Something wrong when execute action: {exception}")
            traceback.print_exc()
            execute_action_output.setIsDone(True)
        finally:
            if final_submit:
                execute_action_output.setIsDone(True)
                self._inputValueHandler.next(target_url, form_xpath)
        return execute_action_output

    def _is_legal_directive(self):
        episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
        episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
        states = episode_handler.getAllState()
        # When the length of states is less than 2, it means that the current state is the first state
        # or the app element is none and then final submit and the is_legal directive is false in this case
        # episode_handler.remain_only_index_zero_state() will remove states so that the length of states is less than 2
        if len(states) < 2:
            return False
        if states[-2].getActionType() == "click" and states[-2].getInteractedElement():
            interactive_app_element: AppElement = states[-2].getInteractedElement()
            tag_name = interactive_app_element.getTagName()
            tag_type = interactive_app_element.getType()
            if tag_name == "button" or tag_name == "a" or (tag_name == 'input' and (
                    tag_type == 'submit' or tag_type == "button" or tag_type == 'image')):
                after_action_dom = states[-1].getDOM()
                before_action_dom = states[-2].getDOM()
                return self._directive_rule_service.isLegal(self._target_page_id, before_action_dom, after_action_dom)
        return False

    def _remove_target_page(self):
        remove_target_page_use_case = RemoveTargetPageUseCase()
        remove_target_page_input = RemoveTargetPageInput(self._target_page_id)
        remove_target_page_output = RemoveTargetPageOutput()
        remove_target_page_use_case.execute(remove_target_page_input, remove_target_page_output)
        return remove_target_page_output

    def _reset_environment(self) -> ResetEnvironmentOutput:
        reset_env_use_case = ResetEnvironmentUseCase(self.__aut_operator)
        reset_env_use_input = ResetEnvironmentInput(self._episodeIndex)
        reset_env_use_output = ResetEnvironmentOutput()
        try:
            reset_env_use_case.execute(reset_env_use_input, reset_env_use_output)
            return reset_env_use_output
        except NosuchElementException:
            raise NosuchElementException("NoSuchElementException when reset environment")
        except RuntimeError:
            self.__aut_controller.resetAUTServer(True)
            reset_env_use_case.execute(reset_env_use_input, reset_env_use_output)

    def _get_default_value(self, url: str, high_level_action: HighLevelAction) -> Optional[HighLevelAction]:
        # Check if the xpath is in the default value
        result = HighLevelAction.fromHighLevelAction(high_level_action)
        # Get default input values
        default_value_list = self._default_value_fetcher.get_xpath_default_value_dict(url)
        if default_value_list is None:
            return None
        for xpath, default_value in default_value_list.items():
            result.append(AppEvent(xpath, default_value, 1))
        return result
