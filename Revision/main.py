import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from utils import call_agent_async
from memory_agent.agent import memory_agent

load_dotenv()

# ===== PART 1: Initialize Persistent Session Service =====
# Using SQLite database for persistent storage
db_url = "sqlite:///.//my_agent_data.db"
session_service = DatabaseSessionService(db_url == db_url)


# ===== PART 2: Define Initial State =====
# This will only be used when creating a new session
initial_state = {
    "user_name": "Ketan Raj",
    remidnders: [],
}

### === PART 3: Session Management - Find or Create === ###

async def main_sync():
    # Setup constants
    APP_NAME = "Memory Agent"
    USER_ID = "ketanraj"
    # Check for existing sessions for this user
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    # If there's an existing session, use it, otherwise create a new one
    if existing_sessions and len(existing_sessions.sessions)>0:
        # Use the most recent session
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        # Create a new session with inttial state
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")

    print("\nWelcome to Memory Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    # ===== PART 4: Agent Runner Setup =====
    # Create a runner with the memory agent

    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    # ===== PART 5: Interactive Conversation Loop =====
    while True:
        #Get user input
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the conversation. Goodbye!")
            break
        # Call the agent asynchronously with the user's query
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


if __name__ == "__main__":
    # Run the main function in an event loop
    asyncio.run(main_sync())

