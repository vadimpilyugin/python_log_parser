from . import log_formats as fmt
from . import service as srv
from . import excp
from . import aggregation as agg
from . import fields
from .config import config

import yaml
import os
import re

def content(fn):
  with open(fn, 'r', encoding='utf-8') as f:
    return yaml.load(f)

def normalize(s):
  return s.replace('(?<', '(?P<')

def load_log_formats(content):
  log_formats = []
  for fmt_name, params in content.items():
    log_formats.append(
      fmt.LogFormat(
        name=fmt_name,
        service=params[fields.SERVICE] if fields.SERVICE in params else None,
        date=params[fields.DATE],
        regex=re.compile(normalize(params[fields.REGEX]), re.X)
      )
    )
  return fmt.LogFormatSet(log_formats)

def template_iterator(content):
  for level in content:
    for category in content[level]:
      for template in content[level][category]:
        yield(level, category, template)

def load_service(content):
  assert 'service' in content, excp.NO_SERVICE_NAME
  assert 'regex' in content, excp.NO_REGEX
  assert 'templates' in content, excp.NO_TEMPLATES

  service_templates = []
  if content['templates'] is None:
    content['templates'] = []
  categories = {}
  for level, category, template in template_iterator(content['templates']):
    service_templates.append(
      srv.Template(
        regex_s=normalize(template),
        category=category,
        level=level,
      )
    )
    categories[category] = True
  return srv.Service(
    regex=re.compile(normalize(content['regex'])),
    name=content['service'],
    service_templates=srv.ServiceTemplates(service_templates),
    categories=categories
  )

def load_all_services(dir):
  services = []
  for fn in filter(lambda x: re.match(r'.*\.yml', x), os.listdir(dir)):
    services.append(load_service(content(os.path.join(dir,fn))))
  return srv.ServiceSet(services)

def load_aggregations():
  report_content = content(config["report_file"])
  rprt = agg.Report()
  for server, stat_types in report_content.items():
    for stat_type, stats in stat_types.items():
      for stat in stats:
        if stat_type == fields.COUNTERS:
          stat = agg.Counter(stat)
        else:
          stat = agg.Aggregation(stat)
        rprt.add_stat(server, stat_type, stat)
  return rprt