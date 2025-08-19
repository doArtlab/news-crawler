from openai import OpenAI
from common.config import Config

client = OpenAI(api_key=Config.openai_api_key)

def generate_text(instruction: str, input: str, model: str = "gpt-5-mini") -> str:
    """
    Generate text using OpenAI's API.

    Args:
        instruction (str): The instruction for the model.
        input (str): The input text to be processed.
        model (str): The model to use for generation.

    Returns:
        str: The generated text.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": input}
        ]
    )
    return response.choices[0].message.content.strip() if response.choices else ""