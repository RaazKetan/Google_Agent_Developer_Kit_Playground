import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openai/gpt-4.1",
    api_key = os.getenv("OPENAI_API_KEY"),
)

def get_dad_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Did you hear about the claustrophobic astronaut? He just needed a little space.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I used to play piano by ear, but now I use my hands."
    ]
    return random.choice(jokes)


root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="An agent that tells dad jokes.",
    instruction="""
    You are a helpful assistant that tells dad jokes.
    Only use the tool `get_dad_joke` to respond to the user.
    """,
    tools=[get_dad_joke],
)