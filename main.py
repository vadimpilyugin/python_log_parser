import re
import fields
from template import TemplateLoader
import pprint

pp = pprint.PrettyPrinter(indent=2)

# _LogFormats = {
#   r'QQ' : { 
#     fields.LOG_FORMAT: 'ApacheFormat',
#     fields.SERVICE_GROUP : 'apache' 
#   },
#   r'QQRQ' : { 
#     fields.LOG_FORMAT : 'SyslogFormat'
#   },
#   r'QRQRQ' : {
#     fields.LOG_FORMAT : 'Fail2BanFormat',
#   }
# }

# _LogFormats = dict((re.compile(name), val) for name, val in _LogFormats.items())

# _ServiceGroups = {
#   r'QQ\d' : {
#     fields.SERVICE_GROUP : 'QQ',
#     fields.TEMPLATES : [
#       ({fields.TEMPLATE_REGEX : r'QQRQ', fields.LEVEL : 'Info', TEMPLATE_CATEGORY : 'Tor uptime stats', fields.TEMPLATE_ID : 203}, 200),
#       ({fields.TEMPLATE_REGEX : r'QRRQ', fields.LEVEL : 'Info', TEMPLATE_CATEGORY : 'Tor downtime stats', fields.TEMPLATE_ID : 201}, 150)
#     ]
#   }
# }

def find_regex(logline, regexes):
  for rgx in regexes:
    md = rgx.match(logline)
    if md:
      return rgx
  return None

class LogFormatParser:
  def __init__(self, log_formats):
    self.log_formats = log_formats
    self.cached_log_format = None

  def parse(self, logline):
    md = None
    if self.cached_log_format:
      md = self.cached_log_format.match(logline)
    if not self.cached_log_format or md is None:
      rgx = find_regex(logline, self.log_formats)
      if rgx is None:
        return Parser.NO_LOG_FORMAT
      self.cached_log_format = rgx
      return rgx.match(logline)

class Parser:
  OK = 0
  NO_LOG_FORMAT = 1
  NO_SERVICE_GROUP = 2
  NO_TEMPLATE = 3
  ATTRIBUTE_CLASHING = 4

  strerror = {
    OK : 'OK',
    NO_LOG_FORMAT : "Log format not found",
    NO_SERVICE_GROUP : "No service group found",
    NO_TEMPLATE : "No template found",
    ATTRIBUTE_CLASHING : "Attributes in linedata clash with attributes from log_format"
  }

  @staticmethod
  def _retcode(errno, match_data = None):
    hsh = {
      fields.OK : errno == Parser.OK, 
      fields.ERRNO : errno, 
      fields.DESCR : Parser.strerror[errno]
    }
    if match_data:
      hsh[fields.MATCH_DATA] = match_data
    return hsh

  def __init__(self, log_formats, service_groups):
    self.service_groups = service_groups
    self.log_format_parser = LogFormatParser(log_formats)

  def parse(self, loglines):
    cached_log_format = None
    cached_service_names = {}
    for logline in loglines:
      md = None
      if cached_log_format:
        md = cached_log_format.match(logline)
      if not cached_log_format or md is None:
        for log_format in self.log_formats:
          md = log_format.match(logline)
          if md:
            cached_log_format = log_format
            break
        if md is None:
          yield(Parser._retcode(Parser.NO_LOG_FORMAT))
          continue
      assert(md is not None)
      assert(cached_log_format is not None)
      hsh = md.groupdict()
      if not fields.MESSAGE in hsh:
        msg = logline
      else:
        msg = hsh[fields.MESSAGE]
      if not fields.SERVICE in hsh:
        try:
          service = self.log_formats[cached_log_format][fields.SERVICE]
        except KeyError:
          print(self.log_formats[cached_log_format])
          raise
      else:
        service = hsh[fields.SERVICE]
      if not service in cached_service_names:
        for group_rgx, service_group in self.service_groups.items():
          md = group_rgx.match(service)
          if md:
            cached_service_names[service] = service_group
            break
        if not service in cached_service_names:
          yield(Parser._retcode(Parser.NO_SERVICE_GROUP, match_data=hsh))
          continue
      assert(service in cached_service_names)
      service_group = cached_service_names[service]
      hsh[fields.SERVICE_GROUP] = service_group[fields.SERVICE_GROUP]
      md = None
      for template,_ in cached_service_names[service][fields.TEMPLATES]:
        md = template[fields.TEMPLATE_REGEX].match(msg)
        if md:
          hsh.update(template)
          break
      if not md:
        yield(Parser._retcode(Parser.NO_TEMPLATE, match_data=hsh))
        continue
      assert(md is not None)
      linedata = md.groupdict()
      if not hsh.keys().isdisjoint(linedata.keys()):
        attribute_clashing = None
        for k,v in hsh.items():
          if k in linedata and v != linedata[k]:
            hsh[fields.LINEDATA] = linedata
            attribute_clashing = True
            print(k, v)
            break
        if attribute_clashing:
          yield(Parser._retcode(Parser.ATTRIBUTE_CLASHING, match_data=hsh))
          continue
      hsh.update(linedata)
      yield(Parser._retcode(Parser.OK, match_data=hsh))

t = TemplateLoader(dir="templates")
p = Parser(
  t.load_log_formats("log_formats.yml"),
  t.load_all_service_groups()
)

with open("logs/access.log") as f:
  ar = f.readlines()
c = 0
for i in p.parse(ar):
  pp.pprint(ar[c])
  pp.pprint(i)
  input(">>>>>>>>>>>>>\n")
  c += 1