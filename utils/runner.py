from abc import ABC, abstractmethod
from typing import Optional
from utils import get_random_prompt, LLMFreeHitBaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted


class LLMChat(ABC):
    """
    Abstract class for chat model classes of langchain packages like ChatOpenAI, ChatGoogleGenerativeAI.
    """

    @abstractmethod
    def invoke(self, prompt):
        pass


class LLMRunner:
    def __init__(self, logger, llm: LLMChat, model_info: dict, provider='Gemini'):
        self.logger = logger
        self.llm = llm
        self.model_info = model_info
        self.provider = provider
        self.current_model = model_info[0]['name']
        self._add_extra_args()

    def _add_extra_args(self):
        for model in self.model_info:
            model['count'] = 0

    def _get_llm(self, model_name: Optional[str] = None):
        try:
            if self.provider == 'Gemini':
                llm = ChatGoogleGenerativeAI(model=model_name)
                return llm
        except Exception as e:
            self.logger.error(f"Error in get_llm: {e}")
            return False

    def _get_structured_output_llm(self, model_name: Optional[str] = None):
        llm = self._get_llm(model_name=model_name)
        so_llm = llm.with_structured_output(LLMFreeHitBaseModel)
        return so_llm

    def _call_llm(self, llm):
        try:
            prompt = get_random_prompt()
            result = llm.invoke(prompt)
            return result
        except Exception as e:
            self.logger.error(f"Error in call_llm: {e}")
            return False

    def run(self, prompt):
        while True:
            try:
                self._call_llm()
                break
            except ResourceExhausted as e:
                print(f"ResourceExhausted error occurred: {e}. Retrying...")
