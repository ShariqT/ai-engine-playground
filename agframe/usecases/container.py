class Error:
  def __init__(self, data):
    self.data = data
  def __str__(self):
    return str(self.data)

class Container:
  def __init__(self, steps, name):
    self.name = name
    self.steps = steps
    self.failed = False
    self.failed_reason = None
    self.failed_index = None
    self.failed_rollback = False
    self.failed_rollback_reason = False
    self.returned_value = {}
    self.command = None

  def input(self, command):
    self.command = command
    return self.start()

  def start(self):
    try:
      for idx, step in enumerate(self.steps):
        result = step.do(self.returned_value, self.command.request)
        if result is not None:
          for key in result.keys():
            if key in self.returned_value.keys():
              self.returned_value[key] = [self.returned_value[key]] + [result[key]]
            else:
              self.returned_value.update(result)
      return self.returned_value
    except Exception as e:
      self.failed = True
      failed_action_name = self.steps[idx].name
      self.failed_reason = f"Failed action: {failed_action_name} because of {str(e)}"
      self.failed_index = idx
      return self.rollback()
  
  def rollback(self):
    steps_to_rollback = self.steps[0:self.failed_index + 1]
    try:
      for step in steps_to_rollback:
        step.rollback()
      self.returned_value = {}
      return Error({
        "failure": f"{self.name} failed processing",
        "failure_reason": self.failed_reason
      })
    except Exception as e:
      self.failed_rollback = True
      self.failed_rollback_reason = str(e)
      return Error({
        "failure": f"{self.name} failed processing", 
        "failure_reason": self.failed_reason,
        "failed_rollback": self.failed_rollback_reason
      })
    

      

