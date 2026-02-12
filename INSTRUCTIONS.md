Follow the overview of the agframe library:
## Core Components

### 1. Container (`agframe.usecases.container.Container`)
The main orchestrator/pipeline executor.

- **Purpose**: Executes a sequence of Actions (steps) in order, passing accumulated results between them
- **Key behaviors**:
  - Receives a `Command` via `input()` method
  - Iterates through `steps` (Actions), calling `do(context, request)` on each
  - Accumulates return values from each step into `returned_value` dict
  - If a key already exists, converts it to a list and appends new values
  - On any exception: triggers `rollback()` on all previously executed steps
  - Returns either the accumulated results dict or an `Error` object

### 2. Action (`agframe.actions.action.Action`)
Base class for individual steps in the pipeline.

- **Purpose**: Represents a single unit of work in the pipeline
- **Interface**:
  - `do(context, request)` - Execute the action's logic; receives accumulated context and original request
  - `rollback()` - Undo the action's effects (called on failure)
- **Note**: Actions are described as "steps that do things with tasks, like access a file, or make an API request"

### 3. Command (`agframe.commands.command.Command`)
Input wrapper that carries the initial request data.

- **Purpose**: Encapsulates the request/input data passed into the pipeline
- **Interface**:
  - `make_request(data)` - Sets the request payload

### 4. Task (`agframe.tasks.task.Task`)
Abstract base for actual work units.

- **Purpose**: Performs the actual operations (API calls, file I/O, etc.)
- **Interface**:
  - `execute(event, data)` - Executes the task logic

### 5. Error (`agframe.errors.error.Error`)
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
class AddNumber(Action):
    def __init__(self, name):
        self.name = name
        self.mathtask = MathTask()
    def do(self, context, request):
        left = request.get("left")
        right = request.get("right")
        result = self.mathtask.execute("add", {"left": left, "right": right})
        return {"number": result['answer']}
    def rollback(self):
        pass
# Define tasks
class MathTask(Task):
    def execute(self, event, data):
        if event == "add":
            return {"answer": data['left'] + data['right']}
        if event == "subtract":
            return {"answer": data['left'] + data['right']}

# Build pipeline
steps = [AddNumber("step1"), AnotherAction("step2")]
container = Container(steps, "my-use-case")
command = Command("process")

# Execute
command.make_request({"left": 1, "right": 2})
result = container.input(command)  # Returns {"number": 3, ...} or Error
```

Before writing new code, always follow the following rules:
- New commands should subclass the agframe.command.Command class and go inside of the commands folder. 
- New actions should subclass the agframe.actions.Action class and go inside of the actions folder. 
- New tasks should subclass the agframe.tasks.Task class and go inside of the tasks folder.
