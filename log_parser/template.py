import yaml
import re
from os import path
import os
from . import fields

class TemplateLoader:
  EXT = r'\.yml'

  def __init__(self, dir="./"):
    self.regex_id = 1
    self.directory = dir

  def loc(self, fn):
    return path.normpath(path.join(self.directory, fn))

  def to_fn(self, service_group):
    return self.loc(service_group+TemplateLoader.EXT)

  @staticmethod
  def load_file(fn):
    with open(fn) as f:
      return yaml.load(f)

  @staticmethod
  def replace_template_string(template):
    return template.replace('(?<', '(?P<')

  @staticmethod
  def replace_template_strings(templates):
    for warning_level in templates:
      for category in templates[warning_level]:
        templates[warning_level][category] = list(
          map(
            lambda template: template.replace('(?<', '(?P<'), 
            templates[warning_level][category]
          )
        )


  @staticmethod
  def compile_templates(templates):
    for warning_level in templates:
      for category in templates[warning_level]:
        templates[warning_level][category] = list(
          map(
            lambda template: re.compile(template), 
            templates[warning_level][category]
          )
        )

  def flatten_templates(self, templates):
    ar = []
    for warning_level in templates:
      for category in templates[warning_level]:
        for template_regex in templates[warning_level][category]:
          ar.append(
            (
              {
                fields.TEMPLATE_REGEX : template_regex, 
                fields.LEVEL : warning_level, 
                fields.TEMPLATE_CATEGORY : category, 
                fields.TEMPLATE_ID : self.regex_id
              },
              0 # number of matches
            )
          )
          self.regex_id += 1
    return ar

  def load_service_group(self, service_group):
    hsh = TemplateLoader.load_file(self.loc(service_group))
    TemplateLoader.replace_template_strings(hsh['templates'])
    TemplateLoader.compile_templates(hsh['templates'])
    templates = self.flatten_templates(hsh['templates'])
    group_regex = re.compile(hsh['regex'])
    return group_regex, {
      fields.SERVICE_GROUP : hsh['service'],
      fields.TEMPLATES : templates
    }

  def load_all_service_groups(self):
    service_groups = dict()
    rgx = re.compile(r'.*'+TemplateLoader.EXT)
    for service_group in filter(lambda x: rgx.match(x), os.listdir(self.directory)):
      group_regex, group_attrs = self.load_service_group(service_group)
      service_groups[group_regex] = group_attrs
    return service_groups

  @staticmethod
  def sort_templates(service_groups):
    for group_regex in service_groups:
      service_groups[group_regex][fields.TEMPLATES].sort(lambda x: -x[1])

  def load_log_formats(self, fn):
    hsh = TemplateLoader.load_file(fn)
    log_formats = {}
    for key in hsh:
      rgx = re.compile(TemplateLoader.replace_template_string(hsh[key]['regex']), re.X)
      log_formats[rgx] = {
        fields.LOG_FORMAT : key,
      }
      if fields.SERVICE in hsh[key]:
        log_formats[rgx][fields.SERVICE] = hsh[key][fields.SERVICE]
    return log_formats
