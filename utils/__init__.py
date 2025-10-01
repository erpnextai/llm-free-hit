from utils.constant import QUESTIONS, PROMPT
import random
from utils.logger import get_logger
from pydantic import BaseModel, Field
from typing import List


class LLMFreeHitBaseModel(BaseModel):
    response: str = Field(..., description="Generate content based on the input & Instructions provided.")


def get_random_prompt() -> str:
    """
    Generates a random prompt by selecting a random question from a predefined list
    and formatting it into a prompt template.

    Returns:
        str: A formatted prompt string containing a randomly selected question.
    """
    random_question = random.choice(QUESTIONS)
    prompt = PROMPT.format(question=random_question)
    return prompt


__all__ = ["get_random_prompt", "LLMFreeHitBaseModel", "get_logger"]
