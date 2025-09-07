# LLM Free Hit

A script for checking Free Hit functionality.

## Prerequisites

- Python 3.10.6

## Quick Start

1. **Create a Python virtual environment**:
    ```bash
    python -m venv .venv
    ```

2. **Activate the virtual environment**:
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the script**:
    ```bash
    python main.py --provider Gemini
    ```

# .env
The `.env` file should contain the following environment variables:

```bash
GOOGLE_API_KEY=your_api_key_here

OUTPUT_DIR=output
```