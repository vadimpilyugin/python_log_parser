import yaml
from . import log_formats as fmt
from . import service as srv
import os
import re
from . import excp
from . import aggregation as agg
from .config import config
from .config import abs_path
from . import fields

TEMPLATE_ID = 1

def content(fn):
  with open(abs_path(fn), 'r', encoding='utf-8') as f:
    return yaml.load(f)

def normalize(s):
  return s.replace('(?<', '(?P<')

def load_log_formats(content):
  log_formats = []
  for fmt_name in content:
    log_formats.append(
      fmt.LogFormat(
        name=fmt_name,
        regex=re.compile(normalize(content[fmt_name]['regex']), re.X),
        service=content[fmt_name]['service'] if 'service' in content[fmt_name] else None,
        date=content[fmt_name]['date'] if 'date' in content[fmt_name] else None 
      )
    )
  return fmt.LogFormatSet(log_formats)

def template_iterator(content):
  for level in content:
    for category in content[level]:
      for template in content[level][category]:
        yield(level, category, template)

def load_service(content):
  global TEMPLATE_ID
  service_templates = []
  if 'templates' not in content:
    raise excp.LoaderException(content)
  if content['templates'] is None:
    content['templates'] = []
  categories = {}
  for level, category, template in template_iterator(content['templates']):
    service_templates.append(
      srv.Template(
        regex_s=normalize(template),
        category=category,
        level=level,
        template_id=TEMPLATE_ID
      )
    )
    TEMPLATE_ID += 1
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
  with open(abs_path(config["report_file"]), 'r', encoding='utf-8') as f:
    content = yaml.load(f)
  for server_name in content:
    for stat_type in content[server_name]:
      ar = content[server_name][stat_type]
      for i in range(0, len(ar)):
        if stat_type == fields.COUNTERS:
          ar[i] = agg.Counter(ar[i])
        elif stat_type == fields.DISTRIBUTIONS:
          ar[i] = agg.Aggregation(ar[i])
  return content