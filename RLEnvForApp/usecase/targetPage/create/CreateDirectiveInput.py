from RLEnvForApp.usecase.targetPage.HighLevelActionList import HighLevelActionList

class CreateDirectiveInput:
    def __init__(self, targetPageId: str, episodeHandlerId: str, highLevelActionList: HighLevelActionList):
        self._targetPageId = targetPageId
        self._episodeHandlerId = episodeHandlerId
        self._highLevelActionList = highLevelActionList

    def getTargetPageId(self):
        return self._targetPageId

    def getEpisodeHandlerId(self):
        return self._episodeHandlerId

    def getHighLevelActionList(self):
        return self._highLevelActionList
