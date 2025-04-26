from RLEnvForApp.domain.llmService.TestCombinationOutputResponse import TestCombinationOutputResponse
from RLEnvForApp.usecase.targetPage.FormInputValueList import FormInputValueList


class LlmTestCombinationToFormInputValueListConverter:
    def convert(self, test_combination:TestCombinationOutputResponse) -> FormInputValueList:
        return FormInputValueList.fromTestCombinationOutputResponse(
            test_combination_output_response=test_combination
        )