from typing import List
from typing_extensions import Annotated, TypedDict
from RLEnvForApp.domain.llmService.FormOutputResponse import FormOutputResponse


class TestCombinationOutputResponse(TypedDict):
    test_combination_list: Annotated[List[FormOutputResponse], "List of test combinations."]
