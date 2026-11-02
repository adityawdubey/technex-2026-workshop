"""
Agent = model (the brain) + instruction (its job) + tools (what it can do).
"""

from google.adk.agents import Agent

"""
The tool: a plain Python function the agent can call.
The LLM only sees its name, docstring and type hints, so keep them clear.
"""
def get_weather(city: str) -> dict:
    """Returns the current weather report for a city."""
    fake_weather = {"goa": "Sunny, 31°C", "manali": "Snowy, -2°C"} #data
    report = fake_weather.get(city.lower())
    if report:
        return {"status": "success", "weather": report}
    return {"status": "error", "message": f"No data for {city}."}

"""
The agent: ADK looks for a variable named `root_agent`.
- model: the LLM (lite version; "gemini-flash-latest" is stronger but was overloaded)
- description: what other agents read about it
- instruction: what this agent follows
- tools: functions it may call (pass the function, don't call it)
"""
root_agent = Agent(
    name="weather_agent",
    model="gemini-flash-lite-latest",
    description="Answers questions about the weather in a city.",
    instruction="You are a friendly weather assistant. "
                "Always use the get_weather tool.",
    tools=[get_weather],
)
