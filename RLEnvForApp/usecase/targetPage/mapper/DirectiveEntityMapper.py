from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import CodeCoverageEntity
from RLEnvForApp.usecase.environment.state.mapper import CodeCoverageEntityMapper
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity
from RLEnvForApp.usecase.targetPage.entity.DirectiveEntity import DirectiveEntity
from RLEnvForApp.usecase.targetPage.mapper import AppEventEntityMapper
from RLEnvForApp.usecase.targetPage.entity.FormInputValueEntity import FormInputValueEntity
from RLEnvForApp.usecase.targetPage.entity.InputValueEntity import InputValueEntity
from RLEnvForApp.usecase.targetPage.FormInputValueList import FormInputValueList
from RLEnvForApp.domain.targetPage.InputValue import InputValue
from RLEnvForApp.domain.targetPage.FormInputValue import FormInputValue
from RLEnvForApp.usecase.targetPage.FormInputValueList import FormInputValueList


def _mappingCodeCoverageEntitiesFrom(odeCoverages: [CodeCoverage]) -> [CodeCoverageEntity]:
    codeCoverageEntities: [CodeCoverageEntity] = []
    for codeCoverage in odeCoverages:
        codeCoverageEntities.append(
            CodeCoverageEntityMapper.mappingCodeCoverageEntityFrom(codeCoverage=codeCoverage))
    return codeCoverageEntities


def _mappingCodeCoverageFrom(codeCoverageEntities: [CodeCoverageEntity]) -> [CodeCoverage]:
    codeCoverages: [CodeCoverage] = []
    for codeCoverageEntity in codeCoverageEntities:
        codeCoverages.append(CodeCoverageEntityMapper.mappingCodeCoverageFrom(
            codeCoverageEntity=codeCoverageEntity))
    return codeCoverages


def _mappingFormInputValueEntitiesFrom(formInputValueList: FormInputValueList) -> [FormInputValueEntity]:
    # TODO: refector this
    formInputValueEntities: list[FormInputValueEntity] = []
    while not formInputValueList.is_done():
        formInputValue: FormInputValue = formInputValueList.get()
        inputValueEntities: list[InputValue] = []
        # Get the input value list from the form input value entity
        for inputValue in formInputValue.getInputValueList():
            xpath: str = inputValue.getXpath()
            value: str = inputValue.getValue()
            action: int = inputValue.getAction()
            inputValueEntities.append(InputValue(xpath=xpath, value=value, action=action))
        pageDom = formInputValue.getPageDom()
        formXPath = formInputValue.getFormXPath()
        # Create a FormInputValueEntity object and append it to the list
        formInputValueEntities.append(FormInputValueEntity(inputValueListEntities=inputValueEntities, page_dom=pageDom, form_xpath=formXPath))
        formInputValueList.next()
    return formInputValueEntities


def _mappingFormInputValueListFrom(formInputValueEntities: [FormInputValueEntity]) -> FormInputValueList:
    # TODO: refector this
    formInputValueList: list[FormInputValue] = []
    for formInputValueEntity in formInputValueEntities:
        inputValueList: list[InputValue] = []
        # Get the input value list from the form input value entity
        inputValueEntityList: [InputValueEntity] = formInputValueEntity.getInputValueListEntities()
        for inputValueEntity in inputValueEntityList:
            xpath:str = inputValueEntity.getXpath()
            value:str = inputValueEntity.getValue()
            action:int = inputValueEntity.getAction()
            inputValueList.append(InputValue(xpath=xpath, value=value, action=action))
        pageDom = formInputValueEntity.getPageDom()
        formXPath = formInputValueEntity.getFormXPath()
        # Create a FormInputValue object and append it to the list
        formInputValueList.append(FormInputValue(*inputValueList, page_dom=pageDom, form_xpath=formXPath))
    return FormInputValueList(formInputValueList)


def mappingDirectiveEntityFrom(directive: Directive) -> DirectiveEntity:
    appEventEntities: [AppEventEntity] = []
    for appEvent in directive.getAppEvents():
        appEventEntities.append(AppEventEntityMapper.mappingAppEventEntityFrom(appEvent=appEvent))
    return DirectiveEntity(url=directive.getUrl(), dom=directive.getDom(), formXPath=directive.getFormXPath(), appEventEntities=appEventEntities, codeCoverageEntities=_mappingCodeCoverageEntitiesFrom(directive.getCodeCoverages()),
                           formInputValueEntities=_mappingFormInputValueEntitiesFrom(directive.getFormInputValueList()))


def mappingDirectiveFrom(directiveEntity: DirectiveEntity) -> Directive:
    appEvents: [AppEvent] = []
    for appEventEntity in directiveEntity.getAppEventEntities():
        appEvents.append(AppEventEntityMapper.mappingAppEventFrom(appEventEntity=appEventEntity))
    return Directive(url=directiveEntity.getUrl(), dom=directiveEntity.getDom(), formXPath=directiveEntity.getFormXPath(), appEvents=appEvents, codeCoverages=_mappingCodeCoverageFrom(directiveEntity.getCodeCoverageEntities()),
                     formInputValueList=_mappingFormInputValueListFrom(directiveEntity.getFormInputValueEntities()))
