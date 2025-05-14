from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.FormInputValueDTO import FormInputValueDTO

class DirectiveDTO:
    def __init__(self, url: str, dom: str, formXPath: str, appEventDTOs: [AppEventDTO], codeCoverageDTOs: [CodeCoverageDTO], formInputValueDTOs: [FormInputValueDTO]):
        self._url = url
        self._dom = dom
        self._formXPath = formXPath
        self._appEventDTOs = appEventDTOs
        self._codeCoverageDTOs = codeCoverageDTOs
        self._formInputValueDTOs = formInputValueDTOs

    def getUrl(self) -> str:
        return self._url

    def getDom(self) -> str:
        return self._dom

    def getFormXPath(self) -> str:
        return self._formXPath

    def getAppEventDTOs(self) -> [AppEventDTO]:
        return self._appEventDTOs

    def getCodeCoverageDTOs(self) -> [CodeCoverageDTO]:
        return self._codeCoverageDTOs

    def getFormInputValueList(self) -> [FormInputValueDTO]:
        return self._formInputValueDTOs
