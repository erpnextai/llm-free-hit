import logging
import os
import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional
from utils import get_random_prompt, LLMFreeHitBaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted, NotFound


class LLMChat(ABC):
    """
    Abstract class for chat model classes of langchain packages like ChatOpenAI, ChatGoogleGenerativeAI.
    """

    @abstractmethod
    def invoke(self, prompt):
        pass


class LLMRunner:
    def __init__(self, logger: logging.Logger, model_info: dict,
                 provider='Gemini', resource_exhausted_retry=25):
        self.logger = logger
        self.model_info = model_info
        self.provider = provider
        self.current_model = model_info[0]
        self.model_length = len(model_info)
        self.resource_exhausted_retry = resource_exhausted_retry
        self._add_extra_args()

        self.test_all_active_models()

    def test_all_active_models(self):
        self.logger.info("Testing all active models...")
        for model in self.model_info:
            if model['is_active']:
                try:
                    llm = self._get_structured_output_llm(model_name=model['name'])
                    prompt = get_random_prompt()
                    result = llm.invoke(prompt)
                    self.logger.info(f"Model {model['name']} response: {result.response}")
                    model['count'] += 1
                except NotFound as e:
                    self.logger.error(f"Model {model['name']} not found: {e}")
                    model['is_active'] = False
                except ResourceExhausted as e:
                    self.logger.error(f"Model {model['name']} resource exhausted: {e}")

    def _add_extra_args(self):
        for model in self.model_info:
            model['count'] = 0

    def _get_llm(self, model_name: Optional[str] = None):
        try:
            if self.provider == 'Gemini':
                llm = ChatGoogleGenerativeAI(model=model_name)
                return llm
            if self.provider == 'Gemma':
                llm = GoogleGemmaChat(model=model_name)
                return llm
        except Exception as e:
            self.logger.error(f"Error in get_llm: {e}")
            raise Exception(f"Error in get_llm: {e}")

    def _get_structured_output_llm(self, model_name: Optional[str] = None):
        llm = self._get_llm(model_name=model_name)
        so_llm = llm.with_structured_output(LLMFreeHitBaseModel)
        return so_llm

    def _call_llm(self, llm):
        prompt = get_random_prompt()
        result = llm.invoke(prompt)
        self.logger.info(f"LLM response: {result.response}")
        return result

    def run(self):
        index = resource_exhausted_retry = 0
        while True:
            model = self.model_info[index]
            try:
                # if the model is not active, skip it
                if not model['is_active']:
                    index += 1
                    if index >= self.model_length:
                        index = 0
                    continue

                llm = self._get_structured_output_llm(model_name=model['name'])
                self._call_llm(llm)
                model['count'] += 1
                self._save_usage()
            except ResourceExhausted as e:
                index += 1
                resource_exhausted_retry += 1
                if index >= self.model_length:
                    index = 0
                if resource_exhausted_retry >= self.resource_exhausted_retry:
                    self._save_usage()
                    break
                self.logger.info(f"ResourceExhausted error occurred: {e}. Retrying...")
            except Exception as e:
                self.logger.error(f"Error occurred: {e}")

    def _save_usage(self):
        output_dir = os.getenv('OUTPUT_DIR', 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, f"{self.provider}_usage.csv")
        df = pd.DataFrame(self.model_info)
        df.to_csv(output_file, index=False)
        self.logger.info(f"Model usage saved to {output_file}")


class GoogleGemmaChat(LLMChat):
    def __init__(self, model: str, api_key: Optional[str] = None):
        from google import genai
        self.genai = genai
        self.client = genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))
        self.model = model

    def invoke(self, prompt: str):
        try:
            contents = [
                self.genai.types.Content(
                    role="user",
                    parts=[self.genai.types.Part.from_text(text=prompt)],
                ),
            ]
            generate_content_config = self.genai.types.GenerateContentConfig()

            # For simplicity, we’ll take only the first response
            response_text = ""
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    response_text += chunk.text

            class Response:
                def __init__(self, response):
                    self.response = response

            return Response(response_text)

        except Exception as e:
            raise Exception(f"Gemma model invocation failed: {e}")

    def with_structured_output(self, output_cls):
        """
        Wrap the invoke output into a structured response using pydantic model
        """
        class StructuredGemmaChat(GoogleGemmaChat):
            def __init__(self, parent):
                self.parent = parent

            def invoke(self, prompt: str):
                raw_response = self.parent.invoke(prompt).response
                try:
                    # Convert to structured output
                    parsed = output_cls(response=raw_response)
                    return parsed
                except Exception:
                    return output_cls(response=raw_response)

        return StructuredGemmaChat(self)
