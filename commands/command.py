
class Command:
  def __init__(self, name):
    self.request = None
    self.name = name

  def make_request(self, data):
    self.request = data