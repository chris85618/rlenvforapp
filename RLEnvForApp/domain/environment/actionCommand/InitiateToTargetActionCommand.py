from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.logger.logger import Logger

from . import IActionCommand


class NosuchElementException(Exception):
    pass


class InitiateToTargetActionCommand(IActionCommand.IActionCommand):
    MAX_RETRY_TIMES = 1

    def __init__(self, appEvents: [AppEvent], rootPath: str, formXPath: str):
        super().__init__(actionNumber=-1, actionType="init")
        self._appEvents = appEvents
        self._rootPath = rootPath
        self._formXPath = formXPath

    def execute(self, operator: IAUTOperator):
        operator.setActionType(super().getActionType())
        isSuccess = False
        retry = 0
        while not isSuccess:
            try:
                Logger().info("Initialize the crawler to the target page")
                Logger().info(f"Root path: {self._rootPath}")
                Logger().info(f"Form XPath: {self._formXPath}")
                operator.resetCrawler(self._rootPath, self._formXPath)
                Logger().info("=====start the initial action=====")
                for appEvent in self._appEvents:
                    xpath = appEvent.getXpath()
                    value = appEvent.getValue()
                    Logger().info(f"Xpath: {xpath}, value: {value}")
                    try:
                        operator.executeAppEvent(xpath=xpath, value=value)
                    except KeyboardInterrupt:
                        Logger.info("KeyboardInterrupt")
                        raise
                    except Exception as exception:
                        Logger().info(f"InitiateToTargetActionCommand: Fail to find Xpath: {xpath}, value: {value}. Ignore...")
                isSuccess = (operator.getElement(self._formXPath) is not None)
                if isSuccess == False:
                    Logger().info(f"InitiateToTargetActionCommand: Fail to locate target form.")
            except KeyboardInterrupt:
                Logger.info("KeyboardInterrupt")
                raise
            except Exception as exception:
                Logger().info(f"InitiateToTargetActionCommand Exception, {exception}")
                retry += 1
            if retry > self.MAX_RETRY_TIMES:
                raise NosuchElementException(f"InitiateToTargetActionCommand Exception, retry {self.MAX_RETRY_TIMES} times")
