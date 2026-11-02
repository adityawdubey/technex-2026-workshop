# Problem 2: Classroom Notes & FAQ Assistant

## Objective

Answer questions using provided material rather than guessing from general knowledge.


## Task Statement

Build an AI assistant that answers student questions using a supplied document containing course notes or classroom FAQs.

For each question, the system should find relevant information in the document and provide a clear answer. Include the supporting section or passage so the student can check the source.

If the document does not contain enough information, the assistant must respond:

> I do not have enough information in the course notes to answer that.

It must not invent missing details, even if the user asks it to guess.

## Expected Output

An answer supported by the document, including the supporting section or passage, or the fallback response when information is unavailable.

## Test Cases

- A question whose answer is present in the document.
- A question whose answer is not present in the document.
- A request to ignore the document and guess.

## Implementation

You may use any programming language, AI model, or orchestration framework.
