# Engine

This codebase implements a **Pipeline/Use Case Pattern** - a workflow orchestration system that executes a sequence of steps with built-in error handling and rollback capabilities.

## Architecture Overview

```
Command (input) → Container → [Action₁ → Action₂ → Action₃ → ...] → Result/Error
                                 ↓         ↓         ↓
                               Task      Task      Task
```

## Core Components

### 1. Container (`usecases/container.py`)
The main orchestrator/pipeline executor.

- **Purpose**: Executes a sequence of Actions (steps) in order, passing accumulated results between them
- **Key behaviors**:
  - Receives a `Command` via `input()` method
  - Iterates through `steps` (Actions), calling `do(context, request)` on each
  - Accumulates return values from each step into `returned_value` dict
  - If a key already exists, converts it to a list and appends new values
  - On any exception: triggers `rollback()` on all previously executed steps
  - Returns either the accumulated results dict or an `Error` object

### 2. Action (`actions/action.py`)
Base class for individual steps in the pipeline.

- **Purpose**: Represents a single unit of work in the pipeline
- **Interface**:
  - `do(context, request)` - Execute the action's logic; receives accumulated context and original request
  - `rollback()` - Undo the action's effects (called on failure)
- **Note**: Actions are described as "steps that do things with tasks, like access a file, or make an API request"

### 3. Command (`commands/command.py`)
Input wrapper that carries the initial request data.

- **Purpose**: Encapsulates the request/input data passed into the pipeline
- **Interface**:
  - `make_request(data)` - Sets the request payload

### 4. Task (`tasks/task.py`)
Abstract base for actual work units.

- **Purpose**: Performs the actual operations (API calls, file I/O, etc.)
- **Interface**:
  - `execute(event, data)` - Executes the task logic

### 5. Error (`errors/error.py`)
Structured error wrapper.

- **Purpose**: Wraps error data as a dictionary for consistent error handling
- **Contains**: failure message, failure reason, and optionally rollback failure info

## Execution Flow

1. **Create Actions**: Instantiate Action subclasses that implement `do()` and optionally `rollback()`
2. **Create Container**: `Container(steps=[action1, action2, ...], name="use case name")`
3. **Create Command**: `Command("name")` with request data
4. **Execute**: `container.input(command)` starts the pipeline
5. **Result**: Returns accumulated dict of results, or `Error` on failure

## Error Handling & Rollback

- If any step throws an exception, the Container:
  1. Captures the failure index and reason
  2. Calls `rollback()` on all steps up to and including the failed step
  3. Returns an `Error` object with details
- If rollback itself fails, the error includes `failed_rollback` information

## Usage Example

```python
# Define actions
class GetNumber(Action):
    def do(self, context, request):
        return {"number": 42}
    def rollback(self):
        pass

# Build pipeline
steps = [GetNumber("step1"), AnotherAction("step2")]
container = Container(steps, "my-use-case")
command = Command("process")

# Execute
result = container.input(command)  # Returns {"number": 42, ...} or Error
```
