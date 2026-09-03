import os
import asyncio
from datetime import datetime, timezone

from dotenv import load_dotenv
from openai import AsyncOpenAI

from app.db import prompts_collection, history_collection

load_dotenv()

PROMPT_NAME = "Education_Prompt"
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


groq_client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def initialize_prompt():
    """
    Creates the required education prompt if it does not already exist.
    """

    prompts_collection.update_one(
        {"_id": PROMPT_NAME},
        {
            "$setOnInsert": {
                "_id": PROMPT_NAME,
                "template": (
                    "You are an expert in education domain. "
                    "Answer the following question clearly and accurately:\n\n"
                    "{{userInput}}"
                )
            }
        },
        upsert=True
    )
def get_prompt_template():
    """
      Retrieves the education prompt template from MongoDB.
    """

    prompt = prompts_collection.find_one(
        {"_id": PROMPT_NAME}
    )
    if not prompt:
        raise RuntimeError("Education_Prompt was not found")
    return prompt["template"]

def build_prompt(user_input):
    """
       Replaces the {{userInput}} placeholder with the user's input.
    """

    template = get_prompt_template()

    return template.replace("{{userInput}}", user_input)

async def ask_ai(user_input):
    """
       Sends one user input to Grok and stores
       the request/response in MongoDB.
    """

    prompt = await asyncio.to_thread(
            build_prompt,
            user_input
        )

    response = await groq_client.responses.create(
        model=GROQ_MODEL,
        input=prompt
    )

    ai_response = response.output_text

    await asyncio.to_thread(
            history_collection.insert_one,
            {
                "prompt_name": PROMPT_NAME,
                "user_input": user_input,
                "prompt": prompt,
                "response": ai_response,
                "created_at": datetime.now(timezone.utc)
            })

    return ai_response