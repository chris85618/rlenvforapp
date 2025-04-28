from typing import List
from pydantic import BaseModel, Field
from RLEnvForApp.domain.llmService.FormOutputResponse import FormOutputResponse


class TestCombinationOutputResponse(BaseModel):
    test_combination_list: List[FormOutputResponse] = Field(..., description="List of test combinations.")
