from . import fields
from . import excp
# from datetime import datetime

NO_SERVICE = "Отсутствует __SERVICE__"

class LogFormat:
  def __init__(self, name, regex, service=None, date=None):
    self.name = name
    self.regex = regex
    if fields.SERVICE not in regex.groupindex and service is None:
      raise excp.LogFormatException(NO_SERVICE)
    self.service = service
    self.date = date

  def parse(self, logline):
    md = self.regex.match(logline)
    if md:
      hsh = md.groupdict()
      if self.service is not None:
        hsh[fields.SERVICE] = self.service
      # if self.date is not None:
      #   hsh[fields.DATE] = datetime.strptime(hsh[fields.DATE], self.date)
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