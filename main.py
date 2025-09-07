from dotenv import load_dotenv
from utils.constant import GEMINI_MODELS
import argparse
from logging import getLogger
from utils.runner import LLMRunner


def main(provider):
    log_filename = f"{provider.lower()}.log"
    logger = getLogger(provider, log_filename)
    if provider == 'Gemini':
        runner = LLMRunner(logger=logger, model_info=GEMINI_MODELS, provider=provider)
        runner.run()
    if provider == 'Groq':
        print("Groq provider is not implemented yet.")


if __name__ == "__main__":
    load_dotenv(override=True)

    parser = argparse.ArgumentParser(description="Run the Gemini script with a specified provider.")
    parser.add_argument("--provider", type=str, choices=["Gemini", "Groq"], required=True, help="Specify the provider name.") # noqa
    args = parser.parse_args()

    provider = args.provider
    main(provider)
