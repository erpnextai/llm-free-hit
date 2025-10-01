QUESTIONS = [
    "Why is the sky blue?",
    "What is the difference between mass and weight?",
    "How does photosynthesis work?",
    "What is the theory of relativity in simple terms?",
    "Why do we see different phases of the Moon?",
    "What is the difference between permutations and combinations?",
    "Why is zero not a natural number?",
    "How do you calculate compound interest?",
    "What is the Pythagorean theorem and why is it important?",
    "What is the difference between mean, median, and mode?",
    "What is the difference between frontend and backend development?",
    "What is recursion in programming?",
    "How does Git differ from GitHub?",
    "What is the difference between a compiler and an interpreter?",
    "What are algorithms and why are they important?",
    "What causes climate change?",
    "How does the internet actually work?",
    "What is artificial intelligence and how is it used today?",
    "What is the difference between renewable and non-renewable energy?",
    "Why do we need cybersecurity?"
]


PROMPT = """
You are a helpful assistant that provides concise and clear answers to user questions. proivde answer less than 500 words.

{question}
""" # noqa

GEMINI_MODELS = [
    {"name": "gemini-2.0-flash-lite", "verbose": "Gemini 2.0 Flash-Lite", "is_active": True},
    {"name": "gemini-2.5-flash-preview-04-17", "verbose": "Gemini 2.5 Flash Preview 04-17", "is_active": False},
    {"name": "gemini-2.0-flash", "verbose": "Gemini 2.0 Flash", "is_active": True},
    {"name": "gemini-2.5-flash-preview-05-20", "verbose": "Gemini 2.5 Flash Preview 05-20", "is_active": False},
    {"name": "gemini-2.5-flash", "verbose": "Gemini 2.5 Flash Preview 05-20", "is_active": True},
    {"name": "gemini-2.5-flash-lite", "verbose": "Gemini 2.5 Flash Preview 05-20", "is_active": True},
    {"name": "gemini-2.5-pro", "verbose": "Gemini 2.5 Flash Preview 05-20", "is_active": True}
]

GEMINI_GEMMA_MODELS = [
    {"name": "gemma-3n-e2b-it", "verbose": "Gemma 3n E2B", "is_active": True},
    {"name": "gemma-3n-e4b-it", "verbose": " Gemma 3n E4B", "is_active": True},
    {"name": "gemma-3-1b-it", "verbose": " Gemma 3 1B", "is_active": True},
    {"name": "gemma-3-4b-it", "verbose": " Gemma 3 4B", "is_active": True},
    {"name": "gemma-3-12b-it", "verbose": "G Gemma 3 12B", "is_active": True},
    {"name": "gemma-3-27b-it", "verbose": "gemma-3-27b-it", "is_active": True}
]
