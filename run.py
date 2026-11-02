"""Chat with an agent in the terminal.

    python run.py               # weather_agent (1 agent + 1 tool)
    python run.py trip_planner  # 3 agents sharing session state
"""
import asyncio
import importlib
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import errors, types

AGENT = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "weather_agent"
if not (Path(__file__).parent / AGENT / "agent.py").exists():
    sys.exit(f"No agent folder called '{AGENT}'. Try: python run.py weather_agent")

load_dotenv(Path(__file__).parent / AGENT / ".env")
root_agent = importlib.import_module(f"{AGENT}.agent").root_agent

APP, USER = AGENT, "student"
RETRYABLE = {429, 500, 503}  # rate limited / Gemini temporarily busy
RETRY_WAITS = [5, 15, 30]  # seconds between attempts
TIMEOUT = 120  # seconds to wait for one full answer before retrying

# ADK logs a full traceback for every failed model call; we print a short message instead.
logging.getLogger("google_adk.google.adk.workflow._node_runner").setLevel(logging.CRITICAL)


def use_model_override(agent) -> None:
    """Optional: GEMINI_MODEL in the agent's .env swaps the model on every LLM agent (handy when one is busy)."""
    if isinstance(agent, LlmAgent):
        agent.model = os.environ["GEMINI_MODEL"]
    for sub in agent.sub_agents:
        use_model_override(sub)


def models_in(agent) -> set:
    found = {agent.model} if isinstance(agent, LlmAgent) else set()
    for sub in agent.sub_agents:
        found |= models_in(sub)
    return found


def check_key() -> None:
    key = os.getenv("GOOGLE_API_KEY", "")
    if not key or key == "PASTE_YOUR_KEY_HERE":
        sys.exit(
            "No Gemini API key found.\n"
            "1. Get a free key: https://aistudio.google.com/apikey\n"
            f"2. Put it in {AGENT}/.env as: GOOGLE_API_KEY=your-key-here"
        )


def short(text: str, n: int = 90) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 3] + "..."


async def ask(runner: Runner, session_id: str, text: str) -> str:
    message = types.Content(role="user", parts=[types.Part(text=text)])
    reply = ""
    async for event in runner.run_async(user_id=USER, session_id=session_id, new_message=message):
        for part in (event.content.parts if event.content else []):
            if part.function_call:
                print(f"  [tool call] {part.function_call.name}({dict(part.function_call.args)})")
            if part.function_response:
                print(f"  [tool result] {part.function_response.response}")
        if event.is_final_response() and event.content and event.content.parts:
            reply = "".join(p.text or "" for p in event.content.parts)
            if event.author != root_agent.name:
                print(f"  [{event.author} finished] {short(reply)}")
    return reply


async def ask_with_retry(runner: Runner, session_id: str, text: str) -> str:
    for attempt, wait in enumerate([0, *RETRY_WAITS], start=1):
        if wait:
            print(f"  [Gemini is busy, retrying in {wait}s...]")
            await asyncio.sleep(wait)
        try:
            return await asyncio.wait_for(ask(runner, session_id, text), TIMEOUT)
        except asyncio.TimeoutError:
            if attempt > len(RETRY_WAITS):
                return f"(no reply after {TIMEOUT}s; Gemini may be overloaded, try again later)"
        except errors.APIError as e:
            if e.code not in RETRYABLE or attempt > len(RETRY_WAITS):
                return f"(error {e.code}: {e.message})"
    return "(no reply)"


async def show_state(sessions: InMemorySessionService, session_id: str) -> None:
    state = (await sessions.get_session(app_name=APP, user_id=USER, session_id=session_id)).state
    if state:
        print("  [session.state]")
        for key, value in state.items():
            print(f"    {key} = {short(value, 70)}")


async def main() -> None:
    check_key()
    if os.getenv("GEMINI_MODEL"):
        use_model_override(root_agent)
    sessions = InMemorySessionService()
    runner = Runner(app_name=APP, agent=root_agent, session_service=sessions)
    session = await sessions.create_session(app_name=APP, user_id=USER)

    model = ", ".join(sorted(models_in(root_agent)))
    print(f"Chatting with {root_agent.name} ({model}). Type 'exit' to quit.\n")
    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text.lower() in {"exit", "quit"}:
            break
        if text:
            answer = await ask_with_retry(runner, session.id, text)
            await show_state(sessions, session.id)
            print(f"Agent: {answer}\n")


if __name__ == "__main__":
    asyncio.run(main())
