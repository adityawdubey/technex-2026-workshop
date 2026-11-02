"""
How agents share information: session state.
Three agents run in order and pass work through a shared whiteboard (session.state).
- output_key="x"  saves an agent's reply into state["x"]   (WRITE)
- {x} inside an instruction is replaced with state["x"]    (READ)
"""

from google.adk.agents import Agent, SequentialAgent

MODEL = "gemini-flash-lite-latest"

"""Step 1: reads the user's destination, WRITES state["destination_facts"]."""
researcher = Agent(
    name="researcher",
    model=MODEL,
    instruction="The user will name a destination. List 5 must-know facts for a "
                "student traveller: top sights, local food, where to stay, "
                "how to get around, one safety tip. Short bullet points.",
    output_key="destination_facts",
)

"""Step 2: READS {destination_facts}, WRITES state["itinerary"]."""
planner = Agent(
    name="planner",
    model=MODEL,
    instruction="Using these facts:\n{destination_facts}\n\n"
                "Write a budget-friendly 3-day itinerary "
                "(Morning / Afternoon / Evening for each day).",
    output_key="itinerary",
)

"""Step 3: READS {itinerary} and writes the final answer for the user."""
packer = Agent(
    name="packer",
    model=MODEL,
    instruction="Based on this itinerary:\n{itinerary}\n\n"
                "Make a packing checklist (max 10 items). "
                "Reply with the itinerary first, then the checklist.",
)

"""SequentialAgent runs them in order: researcher -> planner -> packer."""
root_agent = SequentialAgent(
    name="trip_planner",
    description="Research, plan and pack, sharing results through session state.",
    sub_agents=[researcher, planner, packer],
)
