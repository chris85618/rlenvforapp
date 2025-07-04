from dependency_injector.wiring import Provide, inject

from RLEnvForApp.domain.environment.actionCommandFactoryService.LLMActionCommandFactory import LLMActionCommandFactory
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.actionCommand import IActionCommand
from RLEnvForApp.domain.environment.actionCommandFactoryService import IActionCommandFactoryService
from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator
from RLEnvForApp.domain.environment.observationService.IObservationService import \
    IObservationService
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import \
    IRewardCalculatorService
from RLEnvForApp.domain.environment.state import State
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.environment.executeAction import ExecuteActionInput, ExecuteActionOutput
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository


class ExecuteActionUseCase:
    @inject
    def __init__(self, autOperator: IAUTOperator,
                 episodeHandlerRepository: EpisodeHandlerRepository = Provide[
                     EnvironmentDIContainers.episodeHandlerRepository],
                 rewardCalculatorService: IRewardCalculatorService = Provide[
                     EnvironmentDIContainers.rewardCalculatorService],
                 actionCommandFactory: IActionCommandFactoryService = Provide[
                     EnvironmentDIContainers.actionCommandFactory],
                 observationSerivce: IObservationService = Provide[EnvironmentDIContainers.observationService]):
        self._actionCommandFactory = actionCommandFactory
        self._autOperator = autOperator
        self._observationService = observationSerivce
        self._episodeHandlerRepository = episodeHandlerRepository
        self._rewardCalculatorService = rewardCalculatorService

    def execute(self, input: ExecuteActionInput.ExecuteActionInput, output: ExecuteActionOutput.ExecuteActionOutput):
        episodeHandlerEntity = self._episodeHandlerRepository.findById(input.getEpisodeHandlerId())
        episodeHandler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(
            episodeHandlerEntity=episodeHandlerEntity)

        previousState: State = episodeHandler.getAllState()[-1]
        previousState.setActionNumber(input.getActionNumber())

        if isinstance(self._actionCommandFactory, LLMActionCommandFactory):
            self._actionCommandFactory.setAutName(input.getAutName())
            self._actionCommandFactory.setUrl(input.getUrl())
            self._actionCommandFactory.setXpath(input.getXpath())

        actionCommand: IActionCommand = self._actionCommandFactory.createActionCommand(
            actionNumber=input.getActionNumber(), input_value=input.getValue())
        actionCommand.execute(operator=self._autOperator)

        if input.getActionNumber() == 0:
            previousState.setActionType("click")
        elif input.getActionNumber() == -1:
            previousState.setActionType("changeFocus")
        else:
            previousState.setActionType("input")
            previousState.setAppEventInputValue(actionCommand.getInputValue())

        state: State = self._autOperator.getState()
        observation = self._observationService.getObservation(state=state)
        # state.setOriginalObservation(originalObservation)

        episodeHandler.appendState(state=state)
        self._episodeHandlerRepository.update(
            EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(episodeHandler=episodeHandler))

        codeCoverageDict = {}
        for codeCoverage in state.getCodeCoverages():
            codeCoverageDict[codeCoverage.getCodeCoverageType(
            )] = self._getPercent(codeCoverage.getRatio())
        output.setObservation(observation)
        # output.setOriginalObservation(originalObservation)
        output.setCodeCoverageDict(codeCoverageDict=codeCoverageDict)
        # output.setReward(self._rewardCalculatorService.calculateReward(
            # episodeHandler=episodeHandler))
        output.setCosineSimilarityText(self._rewardCalculatorService.getCosineSimilarityText())
        output.setIsDone(episodeHandler.isDone())

    def _getPercent(self, ratio):
        return ratio * 100

    @classmethod
    def ExecuteActionUseCase(cls, autOperator):
        pass
