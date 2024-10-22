# Next Generation Test Runner - Task 2

This project is part of the test tasks made for the ["Next Generation Test Runner"](https://internship.jetbrains.com/projects/1484/) internship.

## Problem Statement

### Program A: Pseudo-Random Number Generator

Program A will act as a pseudo-random number generator. It reads commands from stdin, where each command is delimited by a line break, and writes responses to stdout. The program should handle the following commands:

- Hi: Responds with "Hi" on stdout.
- GetRandom: Responds with a pseudo-random integer on stdout.
- Shutdown: Gracefully terminates the program.
- Any unknown commands should be ignored.

### Program B: Controller

Program B will launch Program A as a separate process, provided as an argument. Once Program A is running, Program B should:

- Send the Hi command to Program A and verify the correct response.
- Retrieve 100 random numbers by sending the GetRandom command to Program A 100 times.
- Send the Shutdown command to Program A to terminate it gracefully.
- Sort the list of retrieved random numbers and print the sorted list to the console.
- Calculate and print the median and average of the numbers.

## Installation & Usage

### Installing from GitHub

```bash
pip install git+https://github.com/Krat-OS/nxt-gen-test-runner-task-2
```

### Basic Usage

The package provides a simple interface to run the application:

```python
import next_gen_test_runner_task_2

# Run the application
next_gen_test_runner_task_2.run()
```

## Developer Installation Guide

### Prerequisites

- Python 3.11.9 or higher
- pip (Python package installer)

### Installation Steps

#### 1. Create and Activate Virtual Environment

First, create a virtual environment to isolate your project dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 2. Install Hatch

With your virtual environment activated, install Hatch:

```bash
pip install hatch
```

#### 3. Set Up Development Environment

Hatch will automatically create a development environment with all required dependencies when you run any of the project scripts.

## Available Scripts

Run any of these commands from the project root directory:

### Testing and Code Quality

```bash
# Run tests
hatch run test

# Run linter
hatch run lint

# Run formatter
hatch run format

# Run all checks (format, lint, and test)
hatch run check
```

### Running the Application

```bash
# Run the generator
hatch run generator

# Run the controller
hatch run controller
```

### Development Dependencies

The following development tools are automatically installed in your Hatch environment:

- pytest (≥7.0.0) - Testing framework
- pytest-cov (≥4.0.0) - Test coverage reporting
- pytest-asyncio (≥0.21.0) - Async test support
- ruff (≥0.1.0) - Python linter and formatter

### Notes

- The project uses Ruff for both linting and formatting
- Test coverage reports are generated in both terminal output and XML format
- The minimum Python version requirement is 3.11.9
- All development commands are run through Hatch, which manages the development environment automatically
