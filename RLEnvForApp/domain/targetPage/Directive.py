from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.usecase.targetPage.HighLevelActionList import HighLevelActionList


class Directive:
    def __init__(self, url: str, dom: str, formXPath: str, appEvents: [AppEvent], codeCoverages: [CodeCoverage], highLevelActionList: HighLevelActionList):
        self._url = url
        self._dom = dom
        self._formXPath = formXPath
        self._appEvents = appEvents
        self._codeCoverages = codeCoverages
        self._highLevelActionList = highLevelActionList

    def getUrl(self) -> str:
        return self._url

    def getDom(self) -> str:
        return self._dom

    def getFormXPath(self) -> str:
        return self._formXPath

    def getAppEvents(self) -> [AppEvent]:
        return self._appEvents

    def getCodeCoverages(self) -> [CodeCoverage]:
        return self._codeCoverages

    def getCodeCoverageByType(self, codeCoverageType: str) -> CodeCoverage:
        for codeCoverage in self._codeCoverages:
            if codeCoverage.getCodeCoverageType() == codeCoverageType:
                return codeCoverage

    def getHighLevelActionList(self) -> HighLevelActionList:
        return self._highLevelActionList
