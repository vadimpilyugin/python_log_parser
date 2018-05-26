from . import log_formats as fmt
from . import service as srv
from . import loader as ld
from . import fields
import pprint
import os
# from datetime import datetime
# import calendar

pp = pprint.PrettyPrinter(indent=2)

OK = 0
NO_FORMAT = 1
NO_SERVICE = 2
NO_TEMPLATE = 3
FIELDS_CONFLICT = 4

STRERROR = {
  OK : 'OK',
  NO_FORMAT : 'Format not found',
  NO_SERVICE : 'Service not found',
  NO_TEMPLATE : 'Template not found',
  FIELDS_CONFLICT : 'Fields values are conflicting',
}

# class Date:
#   month_dict = {v: k for k,v in enumerate(calendar.month_abbr)}
#   now = datetime.now()
#   now_hsh = {
#     fields.YEAR: now.year,
#     fields.MONTH: now.month,
#     fields.DAY: now.day,
#     fields.HOUR: now.hour,
#     fields.MINUTE: now.minute,
#     fields.SECOND: now.second,
#   }

#   @staticmethod
#   def extract_date(hsh):
#     # Translate string to int
#     if fields.MONTH in hsh and hsh[fields.MONTH] in Date.month_dict:
#       hsh[fields.MONTH] = Date.month_dict[hsh[fields.MONTH]]
#     new_date = {}
#     for k,v in Date.now_hsh.items():
#       if k in hsh:
#         new_date[k] = int(hsh[k])
#       else:
#         new_date[k] = Date.now_hsh[k]
#     return datetime(
#       new_date[fields.YEAR],
#       new_date[fields.MONTH],
#       new_date[fields.DAY],
#       new_date[fields.HOUR],
#       new_date[fields.MINUTE],
#       new_date[fields.SECOND],
#     )

class Parser:
  def __init__(self, log_format_set, service_set, save_line=False,extract_date=False):
    self.log_format_set = log_format_set
    self.service_set = service_set
    self.save_line = save_line
    # self.extract_date = extract_date

  def retcode(self, errno, reason=None, match_data={}):
    hsh = {
      fields.ERRNO : errno, 
      fields.DESCR : STRERROR[errno],
      fields.REASON : reason,
      fields.MATCH_DATA : match_data,
    }
    return hsh

  def parse(self,logline):
    line_hash = self.log_format_set.parse(logline)
    if line_hash is None:
      return NO_FORMAT, logline, {}
    if not fields.MESSAGE in line_hash:
      line_hash[fields.MESSAGE] = logline
    return self.parse_msg(line_hash)
    # if self.extract_date:
    #   hsh[fields.DATE] = Date.extract_date(hsh)

  def parse_msg(self, line_hash):
    service = self.service_set.find_service(line_hash[fields.SERVICE])
    if service is None:
      return NO_SERVICE, service, line_hash
    linedata = service.parse(line_hash[fields.MESSAGE])
    if linedata is None:
      return NO_TEMPLATE, line_hash[fields.MESSAGE], line_hash
    line_hash.pop(fields.MESSAGE)
    for k,v in linedata.items():
      if k in line_hash and line_hash[k] != linedata[k]:
        return FIELDS_CONFLICT, (k, line_hash[k], linedata[k]), line_hash
    line_hash.update(linedata)
    return OK, None, line_hash

  def parsed_logline_stream(self, loglines):
    for logline in loglines:
      errno, reason, match_data = self.parse(logline)
      yield(self.retcode(errno, reason, match_data))

  def parse_dir(self, dir, files={}):
    for fn in os.listdir(dir):
      path = os.path.join(dir,fn)
      with open(path) as f:
        if os.path.isfile(path) and (not files or fn in files):
          for i in self.parsed_logline_stream(f):
            i[fields.MATCH_DATA].update({fields.FILENAME:path})
            yield(i)

  def parse_servers_dirs(self, dir):
    for server_name in os.listdir(dir):
      server_dir = os.path.join(dir,server_name)
      if os.path.isdir(server_dir):
        for i in self.parse_dir(server_dir):
          if fields.SERVER not in i[fields.MATCH_DATA]:
            i[fields.MATCH_DATA][fields.SERVER] = server_name
          yield(i)