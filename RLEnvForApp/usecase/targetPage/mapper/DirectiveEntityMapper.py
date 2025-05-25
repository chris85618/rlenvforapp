from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import CodeCoverageEntity
from RLEnvForApp.usecase.environment.state.mapper import CodeCoverageEntityMapper
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity
from RLEnvForApp.usecase.targetPage.entity.DirectiveEntity import DirectiveEntity
from RLEnvForApp.usecase.targetPage.mapper import AppEventEntityMapper
from RLEnvForApp.usecase.targetPage.entity.HighLevelActionEntity import HighLevelActionEntity
from RLEnvForApp.usecase.targetPage.FormInputValueList import FormInputValueList
from RLEnvForApp.domain.targetPage.HighLevelAction import HighLevelAction


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


def _mappingHighLevelActionEntitiesFrom(formInputValueList: FormInputValueList) -> [HighLevelActionEntity]:
    # TODO: refector this
    highLevelActionEntities: list[HighLevelActionEntity] = []
    while not formInputValueList.is_done():
        highLevelAction: HighLevelAction = formInputValueList.get()
        appEventEntities: list[AppEvent] = []
        # Get the input value list from the form input value entity
        for inputValue in highLevelAction.getInputValueList():
            xpath: str = inputValue.getXpath()
            value: str = inputValue.getValue()
            category: int = inputValue.getCategory()
            appEventEntities.append(AppEvent(xpath=xpath, value=value, category=category))
        pageDom = highLevelAction.getPageDom()
        formXPath = highLevelAction.getFormXPath()
        # Create a HighLevelActionEntity object and append it to the list
        highLevelActionEntities.append(HighLevelActionEntity(appEventEntities=appEventEntities, page_dom=pageDom, form_xpath=formXPath))
        formInputValueList.next()
    return highLevelActionEntities


def _mappingFormInputValueListFrom(highLevelActionEntities: [HighLevelActionEntity]) -> FormInputValueList:
    # TODO: refector this
    highLevelActionList: list[HighLevelAction] = []
    for highLevelActionEntity in highLevelActionEntities:
        inputValueList: list[AppEvent] = []
        # Get the input value list from the form input value entity
        inputValueEntityList: [AppEventEntity] = highLevelActionEntity.getInputValueListEntities()
        for inputValueEntity in inputValueEntityList:
            xpath:str = inputValueEntity.getXpath()
            value:str = inputValueEntity.getValue()
            category:int = inputValueEntity.getCategory()
            inputValueList.append(AppEvent(xpath=xpath, value=value, category=category))
        pageDom = highLevelActionEntity.getPageDom()
        formXPath = highLevelActionEntity.getFormXPath()
        # Create a HighLevelAction object and append it to the list
        highLevelActionList.append(HighLevelAction(*inputValueList, page_dom=pageDom, form_xpath=formXPath))
    return FormInputValueList(highLevelActionList)


def mappingDirectiveEntityFrom(directive: Directive) -> DirectiveEntity:
    appEventEntities: [AppEventEntity] = []
    for appEvent in directive.getAppEvents():
        appEventEntities.append(AppEventEntityMapper.mappingAppEventEntityFrom(appEvent=appEvent))
    return DirectiveEntity(url=directive.getUrl(), dom=directive.getDom(), formXPath=directive.getFormXPath(), appEventEntities=appEventEntities, codeCoverageEntities=_mappingCodeCoverageEntitiesFrom(directive.getCodeCoverages()),
                           highLevelActionEntities=_mappingHighLevelActionEntitiesFrom(directive.getFormInputValueList()))


def mappingDirectiveFrom(directiveEntity: DirectiveEntity) -> Directive:
    appEvents: [AppEvent] = []
    for appEventEntity in directiveEntity.getAppEventEntities():
        appEvents.append(AppEventEntityMapper.mappingAppEventFrom(appEventEntity=appEventEntity))
    return Directive(url=directiveEntity.getUrl(), dom=directiveEntity.getDom(), formXPath=directiveEntity.getFormXPath(), appEvents=appEvents, codeCoverages=_mappingCodeCoverageFrom(directiveEntity.getCodeCoverageEntities()),
                     formInputValueList=_mappingFormInputValueListFrom(directiveEntity.getHighLevelActionEntities()))
