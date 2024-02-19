
from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers


class EpisodeHandlerFactory:
    def __init__(self):
        pass

    def createEpisodeHandler(self, id: str, episodeIndex: int) -> IEpisodeHandler:
        return EnvironmentDIContainers.episodeHandler(id=id, episodeIndex=episodeIndex)
