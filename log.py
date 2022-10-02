import json
import os
from collections import defaultdict

class Logger:
  def __init__(self, path, logsPerWrite = 20):
    self.path = path
    if not os.path.exists(self.path):
      os.mkdir(self.path)
    self.logsPerWrite = logsPerWrite
    self.logsSinceLastWrite = 0
    self.A = {}

  def log(self, name, *args):
    if name not in self.A:
      self.A[name] = []
    self.A[name].append(args)
    self.logsSinceLastWrite += 1
    if self.logsSinceLastWrite >= self.logsPerWrite:
      self.write()

  def write(self):
    for k in self.A:
      with open(os.path.join(self.path, k), 'a+') as f:
        for a in self.A[k]:
          f.write(json.dumps(a) + "\n")
      self.A[k] = []
    self.logsSinceLastWrite = 0
