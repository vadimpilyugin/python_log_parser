import yaml
import log_formats as fmt
import service as srv
import os
import re
import excp

TEMPLATE_ID = 1

def content(fn):
  with open(fn) as f:
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
        service=content[fmt_name]['service'] if 'service' in content[fmt_name] else None
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
  return srv.Service(
    regex=re.compile(normalize(content['regex'])),
    name=content['service'],
    service_templates=srv.ServiceTemplates(service_templates)
  )

def load_all_services(dir):
  services = []
  for fn in filter(lambda x: re.match(r'.*\.yml', x), os.listdir(dir)):
    services.append(load_service(content(os.path.join(dir,fn))))
  return srv.ServiceSet(services)
