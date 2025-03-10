#!/usr/bin/env python3
from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# For Groq-specific models
from langchain_groq import ChatGroq


GROQ_API_KEY="****"


class Groq(ILlmService):
    llm = None

    def __init__(self, model_name="llama-3.3-70b-versatile", temperature=0):
        self.llm = ChatGroq(temperature=temperature, groq_api_key=GROQ_API_KEY,model_name=model_name)

    def get_response(self, prompt: str, **kwargs) -> str:
        # TODO: Improve prompt, maybe add system_prompt, etc...
        response = self.llm.invoke(prompt)
        return response.text()
