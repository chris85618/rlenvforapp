from RLEnvForApp.usecase.targetPage.FormInputValueList import FormInputValueList

class CreateDirectiveInput:
    def __init__(self, targetPageId: str, episodeHandlerId: str, formInputValueList: FormInputValueList):
        self._targetPageId = targetPageId
        self._episodeHandlerId = episodeHandlerId
        self._formInputValueList = formInputValueList

    def getTargetPageId(self):
        return self._targetPageId

    def getEpisodeHandlerId(self):
        return self._episodeHandlerId
    
    def getFormInputValueList(self):
        return self._formInputValueList
