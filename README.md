# Technex 2026 Workshop

Multi-agent systems with Google ADK: example agents and framework-agnostic hands-on exercises.

Two example agents built with [Google ADK](https://adk.dev):

| Agent | What it shows |
|-------|---------------|
| `weather_agent/` | Your first agent: one agent with one tool, `get_weather` |
| `trip_planner/` | How agents share state: researcher, then planner, then packer, passing results through `session.state` |

## 1. Setup (first time only)

Open a terminal in this folder (the one that contains `weather_agent/` and `trip_planner/`), then:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Get a free Gemini API key at https://aistudio.google.com/apikey. Then copy `.env.example` into **each** agent folder as `.env`:

```bash
cp .env.example weather_agent/.env    # Windows: copy .env.example weather_agent\.env
cp .env.example trip_planner/.env     # Windows: copy .env.example trip_planner\.env
```

Open each `.env` and replace `PASTE_YOUR_KEY_HERE` with your key:

```
GOOGLE_API_KEY=your-key-here
```

`.env` files are hidden on macOS because their names start with a dot (press Cmd + Shift + . in Finder to see them). Don't share or commit them.

## 2. Before running

Each time you open a new terminal, go to this folder and activate the environment:

```bash
source .venv/bin/activate          # Windows: .venv\Scripts\activate
```

## 3. Run weather_agent

One agent that calls a Python function as a tool.

```bash
python run.py weather_agent        # terminal chat; shows each tool call and result
```

or with ADK's own commands:

```bash
adk run weather_agent              # ADK terminal chat
adk web                            # browser: open http://localhost:8000, pick weather_agent
```

Try asking:
- "Weather in Goa?" calls the tool and answers "Sunny, 31°C".
- "Weather in Paris?" gets an error from the tool, so the agent apologises.
- "Tell me a joke" makes no tool call.

## 4. Run trip_planner

Three agents in a row, sharing results through `session.state`.

```bash
python run.py trip_planner         # shows each agent finishing and what's in session.state
```

or with ADK's own commands:

```bash
adk run trip_planner               # ADK terminal chat
adk web                            # browser: open http://localhost:8000, pick trip_planner
```

Try typing a city: "Goa", "Jaipur" or "Manali". In `adk web`, open the **State** tab to watch `destination_facts`, then `itinerary`, appear.

## 5. Hands-on exercises

You may use any programming language, AI model, or orchestration framework.

- [Problem 1: The Elevator Pitch Polisher](problem_statement_1.md)
- [Problem 2: Classroom Notes & FAQ Assistant](problem_statement_2.md)
- [Problem 3: The Event Planning Concierge](problem_statement_3.md)

## Tips

- Type `exit` to quit a terminal chat. Press Ctrl+C to stop `adk web`.
- Run every command from this folder, not from inside an agent folder.
- Both agents use `gemini-flash-lite-latest`. To try the stronger `gemini-flash-latest`, change the model line in `weather_agent/agent.py` (`model=`) or `trip_planner/agent.py` (`MODEL =`). If it's busy (error 503), switch back.
