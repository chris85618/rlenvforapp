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
from RLEnvForApp.adapter.agent.model.builder.PromptModelDirector import PromptModelDirector


class InputValuePoolActionCommandFactory(IActionCommandFactoryService):
    def __init__(self):
        super().__init__()
        self.__input_data = inputSpace.inputValues
        self.__input_type = PromptModelDirector.classes

    def createActionCommand(self, actionNumber: int, input_value:str) -> IActionCommand:
        if actionNumber == -1:
            return ChangeFocusCommand(actionNumber=actionNumber)
        elif actionNumber == 0:
            return IRobotClickCommand.IRobotClickCommand(actionNumber)
        else:
            Logger().info(f"Input value: {str(input_value)}")
            return IRobotInputValueCommand.IRobotInputValueCommand(input_value, actionNumber)

    def getActionSpaceSize(self) -> int:
        return len(self.__input_data)

    def getActionList(self) -> [str]:
        return self.__input_data
