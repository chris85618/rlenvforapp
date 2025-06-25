from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import CodeCoverageEntity
from RLEnvForApp.usecase.environment.state.mapper import CodeCoverageEntityMapper
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity
from RLEnvForApp.usecase.targetPage.entity.DirectiveEntity import DirectiveEntity
from RLEnvForApp.usecase.targetPage.mapper import AppEventEntityMapper
from RLEnvForApp.usecase.targetPage.entity.HighLevelActionEntity import HighLevelActionEntity
from RLEnvForApp.usecase.targetPage.HighLevelActionList import HighLevelActionList
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


def _mappingHighLevelActionEntitiesFrom(highLevelActionList: HighLevelActionList) -> [HighLevelActionEntity]:
    # TODO: refactor this
    highLevelActionEntities: list[HighLevelActionEntity] = []
    while not highLevelActionList.is_done():
        highLevelAction: HighLevelAction = highLevelActionList.get()
        appEventEntities: list[AppEventEntity] = []
        # Get the input value list from the form input value entity
        for appEvent in highLevelAction.getAppEventList():
            xpath: str = appEvent.getXpath()
            value: str = appEvent.getValue()
            category: int = appEvent.getCategory()
            appEventEntities.append(AppEventEntity(xpath=xpath, value=value, category=category))
        pageDom = highLevelAction.getPageDom()
        formXPath = highLevelAction.getFormXPath()
        # Create a HighLevelActionEntity object and append it to the list
        highLevelActionEntities.append(HighLevelActionEntity(appEventEntities=appEventEntities, page_dom=pageDom, form_xpath=formXPath))
        highLevelActionList.next()
    return highLevelActionEntities


def _mappingHighLevelActionListFrom(highLevelActionEntities: [HighLevelActionEntity]) -> HighLevelActionList:
    # TODO: refector this
    highLevelActionList: list[HighLevelAction] = []
    for highLevelActionEntity in highLevelActionEntities:
        appEventList: list[AppEvent] = []
        # Get the input value list from the form input value entity
        appEventEntityList: [AppEventEntity] = highLevelActionEntity.getAppEventEntities()
        for appEventEntity in appEventEntityList:
            xpath:str = appEventEntity.getXpath()
            value:str = appEventEntity.getValue()
            category:int = appEventEntity.getCategory()
            appEventList.append(AppEvent(xpath=xpath, value=value, category=category))
        pageDom = highLevelActionEntity.getPageDom()
        formXPath = highLevelActionEntity.getFormXPath()
        # Create a HighLevelAction object and append it to the list
        highLevelActionList.append(HighLevelAction(*appEventList, page_dom=pageDom, form_xpath=formXPath))
    return HighLevelActionList(highLevelActionList)


def mappingDirectiveEntityFrom(directive: Directive, highLevelAction:HighLevelAction = None) -> DirectiveEntity:
    appEventEntities: [AppEventEntity] = []
    for appEvent in directive.getAppEvents():
        appEventEntities.append(AppEventEntityMapper.mappingAppEventEntityFrom(appEvent=appEvent))
    newList = []
    newList.append(highLevelAction)
    highLevelActionList: HighLevelActionList = HighLevelActionList(newList)
    return DirectiveEntity(url=directive.getUrl(), dom=directive.getDom(), formXPath=directive.getFormXPath(), appEventEntities=appEventEntities, codeCoverageEntities=_mappingCodeCoverageEntitiesFrom(directive.getCodeCoverages()),
                           highLevelActionEntities=_mappingHighLevelActionEntitiesFrom(highLevelActionList))


def mappingDirectiveFrom(directiveEntity: DirectiveEntity) -> Directive:
    appEvents: [AppEvent] = []
    for appEventEntity in directiveEntity.getAppEventEntities():
        appEvents.append(AppEventEntityMapper.mappingAppEventFrom(appEventEntity=appEventEntity))
    return Directive(url=directiveEntity.getUrl(), dom=directiveEntity.getDom(), formXPath=directiveEntity.getFormXPath(), appEvents=appEvents, codeCoverages=_mappingCodeCoverageFrom(directiveEntity.getCodeCoverageEntities()),
                     highLevelActionList=_mappingHighLevelActionListFrom(directiveEntity.getHighLevelActionEntities()))
