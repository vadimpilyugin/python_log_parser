from . import fields
import re

SORT_INTERVAL = 5000

class Template:
  template_map = {}
  def __init__(self, regex_s, category, level, template_id):
    self.regex_s = regex_s
    self.regex = re.compile(regex_s)
    self.category = category
    self.level = level
    self.id = template_id
    self.count = 0
    self.hsh = {
      # fields.TEMPLATE_REGEX : regex_s,
      fields.LEVEL : level,
      fields.TEMPLATE_CATEGORY : category,
      fields.TEMPLATE_ID : template_id
    }
    Template.template_map[self.id] = self
  @classmethod
  def get(cls, template_id):
    return cls.template_map[template_id]

  def parse(self, msg):
    md = self.regex.search(msg)
    if md:
      self.count += 1
      hsh = md.groupdict()
      hsh.update(self.hsh)
      return hsh
    return None

class ServiceTemplates:
  def __init__(self, templates=[]):
    self.templates = templates
    self.count = 0

  def __sort(self):
    self.templates.sort(key=lambda x: -x.count)

  def parse(self, msg):
    md = None
    if self.count > SORT_INTERVAL:
      self.__sort()
      self.count = 0
    for template in self.templates:
      md = template.parse(msg)
      if md is not None:
        self.count += 1
        break
    return md

class Service:
  def __init__(self, regex, name, categories={}, service_templates=ServiceTemplates()):
    self.regex = regex
    self.name = name
    self.service_templates = service_templates
    self.categories = categories

  def is_service(self, service_name):
    md = self.regex.match(service_name)
    if md:
      return True
    else:
      return False

  def parse(self, msg):
    return self.service_templates.parse(msg)

  def get_categories(self):
    return list(self.categories.keys()).sort()

  def __repr__(self):
    return self.name

class ServiceSet:
  def __init__(self, services):
    self.cached_services = {}
    self.services = services

  def find_service(self, service_name):
    service = None
    if service_name in self.cached_services:
      service = self.cached_services[service_name]
    if service is None:
      for srv in self.services:
        if srv.is_service(service_name):
          service = srv
          self.cached_services[service_name] = srv
          break
    return service

  def get_services_categories(self):
    return list(
      map(
        lambda x: {fields.NAME: x.name, fields.CATEGORIES:x.get_categories()}, 
        self.services
      )
    ).sort()