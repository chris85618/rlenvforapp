from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from openai import OpenAI

system_prompt = ['You are an AI web crawler assistant. '
                 'Follow the user requirements carefully '
                 'and The user will prompt you for the DOM differences '
                 'before and after submitting the web form. '
                 'Please answer whether the form was submitted successfully. '
                 'Please only say yes or no.',
                 'You are an AI web crawler assistant.'
                 'Follow the user requirements carefully '
                 'and The user will give you some web elements.'
                 'Please answer it is a form submitting button.'
                 'Please only say yes or no.']

class ChatGPTService(ILlmService):
    client = OpenAI(api_key='****')

    def get_response(self, prompt: str, system_prompt: str=None, *args) -> str:
        if system_prompt is None:
            system_prompt = self.get_system_prompt()

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        'role': 'system',
                        'content': system_prompt
                    },
                    {
                        'role': 'user',
                        'content':  prompt
                    }
                ],
                temperature=0,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"ChatGPTService.get_response error: {e}")
