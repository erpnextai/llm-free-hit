import logging
import os
import pandas as pd
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
    def __init__(self, logger: logging.Logger, model_info: dict,
                 provider='Gemini', resource_exhausted_retry=100):
        self.logger = logger
        self.model_info = model_info
        self.provider = provider
        self.current_model = model_info[0]
        self.model_length = len(model_info)
        self.resource_exhausted_retry = resource_exhausted_retry
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
            raise Exception(f"Error in get_llm: {e}")

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

    def run(self):
        index = resource_exhausted_retry = 0
        while True:
            model = self.model_info[0]
            try:
                llm = self._get_structured_output_llm(model_name=model['name'])
                self._call_llm(llm)
                model['count'] += 1
            except ResourceExhausted as e:
                index += 1
                resource_exhausted_retry += 1
                if index >= self.model_length:
                    index = 0
                if resource_exhausted_retry >= self.resource_exhausted_retry:
                    output_dir = os.getenv('OUTPUT_DIR', 'output')
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    output_file = os.path.join(output_dir, f"{self.provider}_usage.csv")
                    df = pd.DataFrame(self.model_info)
                    df.to_csv(output_file, index=False)
                    self.logger.error("Exceeded maximum retries for ResourceExhausted errors.")
                    self.logger.info(f"Model usage saved to {output_file}")
                    break
                self.logger.info(f"ResourceExhausted error occurred: {e}. Retrying...")
