from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.environment.autOperator.mapper import CodeCoverageDTOMapper
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.mapper import AppEventDTOMapper
from RLEnvForApp.usecase.targetPage.dto.InputValueDTO import InputValueDTO
from RLEnvForApp.usecase.targetPage.dto.FormInputValueDTO import FormInputValueDTO
from RLEnvForApp.domain.targetPage.InputValue import InputValue
from RLEnvForApp.domain.targetPage.FormInputValue import FormInputValue
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


def _mappingFormInputValueDTOsFrom(formInputValueList: FormInputValueList) -> [FormInputValueDTO]:
    # TODO: refector this
    formInputValueDTOs: list[FormInputValueDTO] = []
    while not formInputValueList.is_done():
        formInputValue: FormInputValue = formInputValueList.get()
        inputValueDTOList: list[InputValueDTO] = []
        # Get the input value list from the form input value DTO
        for inputValue in formInputValue.getInputValueList():
            xpath: str = inputValue.getXpath()
            value: str = inputValue.getValue()
            action: int = inputValue.getAction()
            inputValueDTOList.append(InputValueDTO(xpath=xpath, value=value, action=action))
        pageDom = formInputValue.getPageDom()
        formXPath = formInputValue.getFormXPath()
        # Create a FormInputValue object and append it to the list
        formInputValueDTOs.append(FormInputValueDTO(input_value_dto_list=inputValueDTOList, page_dom=pageDom, form_xpath=formXPath))
        formInputValueList.next()
    return formInputValueDTOs


def _mappingFormInputValueListFrom(formInputValueDTOs: [FormInputValueDTO]) -> FormInputValueList:
    # TODO: refector this
    formInputValueList: list[FormInputValue] = []
    for formInputValueDTO in formInputValueDTOs:
        inputValueList: list[InputValue] = []
        # Get the input value list from the form input value DTO
        inputValueDTOList: [InputValueDTO] = formInputValueDTO.getInputValueListDto()
        for inputValueDTO in inputValueDTOList:
            xpath:str = inputValueDTO.getXpath()
            value:str = inputValueDTO.getValue()
            action:int = inputValueDTO.getAction()
            inputValueList.append(InputValue(xpath=xpath, value=value, action=action))
        pageDom = formInputValueDTOs.getPageDom()
        formXPath = formInputValueDTOs.getFormXPath()
        # Create a FormInputValue object and append it to the list
        formInputValueList.append(FormInputValue(*inputValueList, page_dom=pageDom, form_xpath=formXPath))
    return FormInputValueList(formInputValueList)


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
                        formInputValueDTOs=_mappingFormInputValueDTOsFrom(directive.getFormInputValueList()))
