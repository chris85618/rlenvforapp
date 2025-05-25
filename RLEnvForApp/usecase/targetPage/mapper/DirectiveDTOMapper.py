from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.environment.autOperator.mapper import CodeCoverageDTOMapper
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.mapper import AppEventDTOMapper
from RLEnvForApp.usecase.targetPage.dto.HighLevelActionDTO import HighLevelActionDTO
from RLEnvForApp.domain.targetPage.HighLevelAction import HighLevelAction
from RLEnvForApp.usecase.targetPage.FormInputValueList import FormInputValueList


def _mappingCodeCoverageDTOsFrom(odeCoverages: [CodeCoverage]) -> [CodeCoverageDTO]:
    codeCoverageDTOs: [CodeCoverageDTO] = []
    for codeCoverage in odeCoverages:
        codeCoverageDTOs.append(
            CodeCoverageDTOMapper.mappingCodeCoverageDTOFrom(codeCoverage=codeCoverage))
    return codeCoverageDTOs


def _mappingCodeCoverageFrom(codeCoverageDTOs: [CodeCoverageDTO]) -> [CodeCoverage]:
    codeCoverages: [CodeCoverage] = []
    for codeCoverageDTO in codeCoverageDTOs:
        codeCoverages.append(CodeCoverageDTOMapper.mappingCodeCoverageFrom(
            codeCoverageDTO=codeCoverageDTO))
    return codeCoverages


def _mappingHighLevelActionDTOsFrom(formInputValueList: FormInputValueList) -> [HighLevelActionDTO]:
    # TODO: refector this
    highLevelActionDTOs: list[HighLevelActionDTO] = []
    while not formInputValueList.is_done():
        highLevelAction: HighLevelAction = formInputValueList.get()
        appEventDTOList: list[AppEventDTO] = []
        # Get the input value list from the form input value DTO
        for inputValue in highLevelAction.getInputValueList():
            xpath: str = inputValue.getXpath()
            value: str = inputValue.getValue()
            category: int = inputValue.getCategory()
            appEventDTOList.append(AppEventDTO(xpath=xpath, value=value, category=category))
        pageDom = highLevelAction.getPageDom()
        formXPath = highLevelAction.getFormXPath()
        # Create a HighLevelAction object and append it to the list
        highLevelActionDTOs.append(HighLevelActionDTO(app_event_dto_list=appEventDTOList, page_dom=pageDom, form_xpath=formXPath))
        formInputValueList.next()
    return highLevelActionDTOs


def _mappingFormInputValueListFrom(highLevelActionDTOs: [HighLevelActionDTO]) -> FormInputValueList:
    # TODO: refector this
    highLevelActionList: list[HighLevelAction] = []
    for highLevelActionDTO in highLevelActionDTOs:
        inputValueList: list[AppEvent] = []
        # Get the input value list from the form input value DTO
        appEventDTOList: [AppEventDTO] = highLevelActionDTO.getInputValueDTOList()
        for appEventDTO in appEventDTOList:
            xpath:str = appEventDTO.getXpath()
            value:str = appEventDTO.getValue()
            category:int = appEventDTO.getCategory()
            inputValueList.append(AppEvent(xpath=xpath, value=value, category=category))
        pageDom = highLevelActionDTOs.getPageDom()
        formXPath = highLevelActionDTOs.getFormXPath()
        # Create a HighLevelAction object and append it to the list
        highLevelActionList.append(HighLevelAction(*inputValueList, page_dom=pageDom, form_xpath=formXPath))
    return FormInputValueList(highLevelActionList)


def mappingDirectiveFrom(directiveDTO: DirectiveDTO) -> Directive:
    appEvents: [AppEvent] = []
    for appEventDTO in directiveDTO.getAppEventDTOs():
        appEvents.append(AppEventDTOMapper.mappingAppEventFrom(appEventDTO=appEventDTO))

    return Directive(url=directiveDTO.getUrl(), dom=directiveDTO.getDom(), formXPath=directiveDTO.getFormXPath(),
                     appEvents=appEvents, codeCoverages=_mappingCodeCoverageFrom(codeCoverageDTOs=directiveDTO.getCodeCoverageDTOs()),
                     formInputValueList=_mappingFormInputValueListFrom(directiveDTO.getFormInputValueList()))


def mappingDirectiveDTOFrom(directive: Directive) -> DirectiveDTO:
    appEventDTOs: [AppEventDTO] = []
    for appEvent in directive.getAppEvents():
        appEventDTOs.append(AppEventDTOMapper.mappingAppEventDTOFrom(appEvent=appEvent))

    return DirectiveDTO(url=directive.getUrl(), dom=directive.getDom(), formXPath=directive.getFormXPath(),
                        appEventDTOs=appEventDTOs, codeCoverageDTOs=_mappingCodeCoverageDTOsFrom(directive.getCodeCoverages()),
                        highLevelActionDTOs=_mappingHighLevelActionDTOsFrom(directive.getFormInputValueList()))
