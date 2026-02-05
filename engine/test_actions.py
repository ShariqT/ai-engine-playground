from actions.action import Action
from tasks.task import Task

class ApiTask(Task):
  def execute(self, event, data):
    return {"data": 8888}


class Action1(Action):
  def __init__(self, name):
    super().__init__(name)
    self.task = ApiTask()
  
  def do(self, context, request):
    return self.task.execute({}, {})



def test_action_with_task():
  a = Action1("test")
  results = a.do({}, {})
  assert 'data' in results.keys()

  
