# Problem 1: The Elevator Pitch Polisher

## Objective

Improve an answer through repeated feedback without getting stuck in an endless revision loop.

## Task Statement

Build an AI assistant that turns a rough idea into a clear, convincing **30-second elevator pitch**.

The user provides an idea and the intended audience. The system writes a first draft, reviews it, and revises it using specific feedback.

The review should check whether the pitch:

- Explains the problem.
- Describes the proposed solution and its value.
- Uses simple language suitable for the audience.
- Stays within **75 words**.

Stop when the pitch meets the checklist or after **three revision rounds**, whichever comes first. If it still falls short, return the best available version and explain what needs improvement.

## Expected Output

- The final pitch.
- A brief explanation of what improved.
- The number of revision rounds.
- Any remaining issues if the revision limit was reached.

## Implementation

You may use any programming language, AI model, or orchestration framework.
