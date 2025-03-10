class ILlmService:
    def get_response(self, prompt: str, **kwargs) -> str:
        """
        Process the prompt and any additional arguments to generate a response.

        Parameters:
        - prompt: The input string for which a response is needed.
        - kwargs: Additional parameters for generating the response.

        Returns:
        - The generated response as a string.
        """
        raise NotImplementedError("This method must be implemented by the subclass.")
