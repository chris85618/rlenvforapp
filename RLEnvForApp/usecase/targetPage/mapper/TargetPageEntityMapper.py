from RLEnvForApp.domain.targetPage import TargetPage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.state.mapper import CodeCoverageEntityMapper
from RLEnvForApp.usecase.targetPage.entity import AppEventEntity, TargetPageEntity
from RLEnvForApp.usecase.targetPage.entity.DirectiveEntity import DirectiveEntity
from RLEnvForApp.usecase.targetPage.mapper import AppEventEntityMapper, DirectiveEntityMapper
from RLEnvForApp.domain.targetPage.HighLevelAction import HighLevelAction


def mappingTargetPageEntityFrom(targetPage: TargetPage.TargetPage, highLevelAction:HighLevelAction = None):
    appEventEntities: [AppEventEntity.AppEventEntity] = []
    for appEvent in targetPage.getAppEvents():
        appEventEntities.append(AppEventEntityMapper.mappingAppEventEntityFrom(appEvent))

    directiveEntities: [DirectiveEntity] = []
    for directive in targetPage.getDirectives():
        directiveEntities.append(
            DirectiveEntityMapper.mappingDirectiveEntityFrom(directive=directive, highLevelAction=highLevelAction))
    return TargetPageEntity.TargetPageEntity(id=targetPage.getId(),
                                             targetUrl=targetPage.getTargetUrl(),
                                             rootUrl=targetPage.getRootUrl(),
                                             appEventEntities=appEventEntities,
                                             taskID=targetPage.getTaskID(),
                                             formXPath=targetPage.getFormXPath(),
                                             basicCodeCoverageEntity=CodeCoverageEntityMapper.mappingCodeCoverageEntityFrom(
                                                 targetPage.getBasicCodeCoverage()),
                                             directiveEntities=directiveEntities)


def mappingTargetPageFrom(targetPageEntity: TargetPageEntity, highLevelAction: HighLevelAction = None):
    if highLevelAction is not None:
        appEvents: [AppEvent] = highLevelAction.getAppEventList()
    else:
        appEvents: [AppEvent] = []
        for appEventEntity in targetPageEntity.getAppEventEntities():
            appEvents.append(AppEventEntityMapper.mappingAppEventFrom(appEventEntity=appEventEntity))
    directives: [Directive] = []
    for directiveEntity in targetPageEntity.getDirectiveEntities():
        directives.append(DirectiveEntityMapper.mappingDirectiveFrom(
            directiveEntity=directiveEntity))
    return TargetPage.TargetPage(id=targetPageEntity.getId(),
                                 targetUrl=targetPageEntity.getTargetUrl(),
                                 rootUrl=targetPageEntity._rootUrl,
                                 appEvents=appEvents,
                                 taskID=targetPageEntity.getTaskID(),
                                 formXPath=targetPageEntity.getFormXPath(),
                                 basicCodeCoverage=CodeCoverageEntityMapper.mappingCodeCoverageFrom(
                                     targetPageEntity.getBasicCodeCoverageEntity()),
                                 directives=directives)
