
# Autonomous AI Teams Program

## Description
This program creates an autonomous team of AI agents with different roles such as CEO, Software Engineer, Code Generator, Data Analyst, and QA Engineer. 
Each role performs specific tasks and communicates through a message queue.

## Dependencies
- gpt4all
- termcolor
- multiprocessing

## Features
- **CEO**: Generates tasks for the Software Engineer.
- **Software Engineer**: Breaks down tasks into sub-tasks.
- **Code Generator**: Generates code snippets for the sub-tasks.
- **Data Analyst**: Analyzes data and provides insights.
- **QA Engineer**: Performs tests and provides results.

## Usage
Run the main program to initiate the AI team. The agents will perform their tasks in a sequential manner, and the results will be printed in the terminal.

### Example Output
```
=== CEO: Design a new feature for the software ===
=== Software Engineer: Create a frontend and a backend component for the new feature ===
=== Code Generator: import React from 'react'; ... ===
=== Data Analyst: The data suggests a high level of user engagement ===
=== QA Engineer: All tests passed. The feature is ready for deployment ===
```
