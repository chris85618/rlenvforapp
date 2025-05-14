from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.FormInputValueList import FormInputValueList


class ITargetPagePort:
    def __init__(self):
        pass

    def connect(self):
        pass

    def close(self):
        pass

    def waitForTargetPage(self):
        pass

    def pullTargetPage(self):
        pass

    def pushTargetPage(self, targetPageId: str, episodeHandlerId: str, formInputValueList: FormInputValueList):
        pass

    def push_target_page_by_directive(self, target_page_id: str, directive_dto: DirectiveDTO):
        pass

    def getPauseAgent(self):
        pass

    def setPauseAgent(self, isPauseAgent: bool):
        pass
