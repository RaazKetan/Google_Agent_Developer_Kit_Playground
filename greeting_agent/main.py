import streamlit as st
import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.adk.events import Event

# --- Step 1: Initialize the agent ---
agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash",
    description="Greets the user",
    instruction="""
    You are a helpful assistant that greets the user. 
    Ask for the user's name and greet them by name.
    """
)

# --- Step 2: Runner + Session setup ---
if "runner" not in st.session_state:
    runner = InMemoryRunner(agent=agent, app_name="streamlit_app")
    st.session_state.runner = runner
    st.session_state.session_id = "session_streamlit"
    st.session_state.user_id = "user_123"

    # ✅ Important: Create session manually (REQUIRED!)
    session = runner.session_service.create_session(
        app_name="streamlit_app",
        user_id=st.session_state.user_id,
        session_id=st.session_state.session_id,
    )
    st.session_state.session_created = True

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🧠 Greeting Agent")

user_input = st.chat_input("Say something...")

# Show past conversation
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# --- Step 3: Run agent asynchronously ---
async def run_agent_async(message: str) -> str:
    response = ""
    async for event in st.session_state.runner.run_async(
        user_id=st.session_state.user_id,
        session_id=st.session_state.session_id,
        new_message=message,
    ):
        if isinstance(event, Event) and event.author != "user":
            if hasattr(event, "parts"):
                response += "".join([part.text for part in event.parts])
    return response.strip()

# --- Step 4: On message submit ---
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("agent"):
        with st.spinner("Thinking..."):
            response = asyncio.run(run_agent_async(user_input))
        st.markdown(response)
        st.session_state.chat_history.append(("agent", response))
