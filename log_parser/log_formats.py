from . import fields
from . import excp
from datetime import datetime

class LogFormat:
  def __init__(self, name, regex, date, service=None):
    self.name = name
    self.regex = regex
    if fields.SERVICE not in regex.groupindex and service is None:
      raise excp.LogFormatException(excp.NO_SERVICE)
    self.date = date
    if fields.DATE not in regex.groupindex:
      raise excp.LogFormatException(excp.NO_DATE)
    self.service = service

  def parse(self, logline):
    md = self.regex.match(logline)
    if md:
      hsh = md.groupdict()
      if self.service is not None:
        hsh[fields.SERVICE] = self.service

      assert fields.SERVICE in hsh, "Cannot find service in logline"

      try:
        hsh[fields.DATE] = datetime.strptime(hsh[fields.DATE], self.date)
      except ValueError:
        print("Wrong date format:", hsh[fields.DATE])
        print()
        return None
      return hsh
    return None

  def __repr__(self):
    return self.name

class LogFormatSet:
  def __init__(self, log_formats):
    self.log_formats = log_formats
    self.cached_format = None

  def parse(self, logline):
    linedata = None
    if self.cached_format:
      linedata = self.cached_format.parse(logline)
    if linedata is None:
      for log_format in self.log_formats:
        linedata = log_format.parse(logline)
        if linedata is not None:
          self.cached_format = log_format
          break
    return linedata

  def __repr__(self):
    return f"{self.log_formats}, cached_format: {self.cached_format}"

  def perf(self, fn, every=5000):
    f = open(fn, 'r')
    now = datetime.now()
    total_lines = 0
    errors = 0
    for index, logline in enumerate(f):
      result = self.parse(logline)
      if result is None:
        errors += 1
        print(logline)
      if index % every == 0:
        print(index, errors)
      total_lines = total_lines + 1
    elapsed = datetime.now() - now
    print(f"--- Lines per second: {total_lines/elapsed.seconds}")