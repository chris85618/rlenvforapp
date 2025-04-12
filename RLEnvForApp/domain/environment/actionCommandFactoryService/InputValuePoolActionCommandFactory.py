import ast
import json
import os
import random

import requests

from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.actionCommand import IRobotClickCommand, IRobotInputValueCommand
from RLEnvForApp.domain.environment.actionCommand.ChangeFocusCommand import ChangeFocusCommand
from RLEnvForApp.domain.environment.actionCommand.IActionCommand import IActionCommand
from RLEnvForApp.domain.environment.actionCommandFactoryService.IActionCommandFactoryService import \
    IActionCommandFactoryService
from RLEnvForApp.domain.environment.inputSpace import ValueWeightSingleton
from RLEnvForApp.logger.logger import Logger


class InputValuePoolActionCommandFactory(IActionCommandFactoryService):
    def __init__(self):
        super().__init__()
        self.__aut_name = ''
        self.__url = ''
        self.__xpath = ''
        self.__input_data = inputSpace.inputValues
        # TODO: self.__input_type = PromptModelDirector.classes

    def createActionCommand(self, actionNumber: int, input_value=None) -> IActionCommand:
        if actionNumber != 0 and actionNumber != -1:
            if input_value is None:
                input_value: str = self._get_input_value(actionNumber)
            Logger().info(f"Input value: {input_value}")
            return IRobotInputValueCommand.IRobotInputValueCommand(input_value, actionNumber)
        elif actionNumber == -1:
            return ChangeFocusCommand(actionNumber=actionNumber)
        return IRobotClickCommand.IRobotClickCommand(actionNumber)

    def _get_input_value(self, action_type: int) -> str:
        # check if the value is in the default_value.json file
        value = self.__check_default_value()
        if value != "":
            return value['value']

        if action_type == 25:
            value = "password"

        return value

    def __check_default_value(self) -> str:
        # open the default_value.json file to check if the value is in the file
        if os.path.exists("default_value.json"):
            with open("default_value.json", "r") as f:
                data = json.load(f)
                # check if the value is in the fil
                if self.__aut_name in data:
                    if self.__url in data[self.__aut_name]:
                        if self.__xpath in data[self.__aut_name][self.__url]:
                            return data[self.__aut_name][self.__url][self.__xpath]
        return ""

    def getActionSpaceSize(self) -> int:
        return len(self.__input_data)

    def getActionList(self) -> [str]:
        return self.__input_data

    def setAutName(self, aut_name: str):
        self.__aut_name = aut_name

    def setUrl(self, url: str):
        self.__url = url

    def setXpath(self, xpath: str):
        self.__xpath = xpath
