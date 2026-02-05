# Actions are the same as the steps in
# the container. Actions do things with
# tasks, like access a file, or make an 
# API request
class Action:
  def __init__(self, name):
    self.name = name
    self.context = None
    self.request = None
  
  def do(self, context, request):
    self.context = context
    self.request = request

  def rollback(self):
    pass