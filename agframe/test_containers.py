from usecases.container import Container, Error
from actions.action import Action
from commands.command import Command

class Action1(Action):
  def do(self, context, request):
    return {"number": 1}
  def rollback(self):
    return True

class Action2(Action):
  def do(self, context, request):
    return {"number": 2}
  
  def rollback(self):
    return True

class Action3(Action):
  def do(self, context, request):
    return {'str': 'string'}

class FailedAction(Action):
  def do(self, context, request):
    raise Exception("failedaction step could not return answer")
  
  def rollback(self):
    return True

class RollbackAction(Action):
  def do(self, context, request):
    raise Exception("failedaction step could not return answer")
  
  def rollback(self):
    raise Exception("rollbackaction failed rollback")
  
def test_steps_processing():
  t = Action1("test")
  do_it = Command("do it")
  steps = [t]
  use_case = Container(steps, "getting emails")
  results = use_case.input(do_it)
  print(f"results is {results}")
  assert results['number'] == 1

def test_multi_step_processing():
  t = Action1("test")
  b = Action2("test1")
  s = Action3("test2")
  steps =[t, b]
  use_case = Container(steps, "getting emails")
  do_it = Command("do it")
  results = use_case.input(do_it)
  assert 'number' in results.keys()
  assert results['number'] == [1, 2]


  use_case2 = Container([t,b,s], "getting folders")
  results = use_case2.input(do_it)
  assert 'number' in results.keys()
  assert results['number'] == [1, 2]
  assert results['str'] == 'string'

def test_failed_step():
  t = Action1("test")
  b = Action2("test1")
  f = FailedAction("test2")
  do_it = Command("do it")

  use_case = Container([t,b,f], "getting emails")
  results = use_case.input(do_it)
  print(results)
  assert type(results) is Error
  assert results.data['failure'] == "getting emails failed processing"
  assert results.data['failure_reason'] == "Failed action: test2 because of failedaction step could not return answer"

def test_step_rollback_failed():
  t = Action1("test")
  z = RollbackAction("no action")
  do_it = Command("do it")
  use_case = Container([t,z], "getting emails")
  results = use_case.input(do_it)
  print(results)
  assert type(results) is Error
  assert "failed_rollback" in results.data.keys()
  assert results.data['failed_rollback'] == "rollbackaction failed rollback"



