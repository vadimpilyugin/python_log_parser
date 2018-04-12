import log_formats as fmt
import service as srv
import loader as ld
import fields
import pprint
import os

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

class Parser:
  def __init__(self, log_format_set, service_set):
    self.log_format_set = log_format_set
    self.service_set = service_set

  def retcode(self, errno, reason=None, match_data={}):
    hsh = {
      fields.ERRNO : errno, 
      fields.DESCR : STRERROR[errno],
      fields.REASON : reason,
      fields.MATCH_DATA : match_data,
    }
    return hsh

  def parse(self,logline):
    hsh = self.log_format_set.parse(logline)
    if hsh is None:
      return NO_FORMAT, logline, {}
    if fields.MESSAGE in hsh:
      msg = hsh[fields.MESSAGE]
      hsh.pop(fields.MESSAGE)
    else:
      msg = logline
    service = self.service_set.find_service(hsh[fields.SERVICE])
    if service is None:
      return NO_SERVICE, service, hsh
    linedata = service.parse(msg)
    if linedata is None:
      return NO_TEMPLATE, msg, hsh
    for k,v in linedata.items():
      if k in hsh and hsh[k] != linedata[k]:
        return FIELDS_CONFLICT, (k, hsh[k], linedata[k]), hsh
    hsh.update(linedata)
    return OK, None, hsh

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

if __name__ == "__main__":
  log_format_set = ld.load_log_formats(ld.content('log_formats.yml'))
  service_set = ld.load_all_services('../../log_parser/services/templates')
  p = Parser(log_format_set, service_set)

  # with open('logs/access.log') as f:
  #   for i in p.parsed_logline_stream(f):
  #     if i[fields.ERRNO] != OK:
  #       pp.pprint(i)
      # assert(i[fields.ERRNO] == OK)

  # with open('logs/sshd.log') as f:
  #   for i in p.parsed_logline_stream(f):
  #     if i[fields.ERRNO] != OK:
  #       pp.pprint(i)
      # input("<<<<<<<<<<<<<<<<<<<<<")

  j = 0
  for i in p.parse_servers_dirs('../../log_parser/logs1'):
    if j % 5000 == 0:
      print(f"Parsed {j} lines")
    if i[fields.ERRNO] != OK:
      pp.pprint(i)
    j += 1