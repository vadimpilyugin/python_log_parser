from . import fields

ASC_SORT = 'asc'
DESC_SORT = 'desc'
TOP = 10

def is_special(k):
  return k[0:2] == '__'

def to_a(hsh, name, sort_order, top):
  global DESC_SORT
  if hsh[fields.TERMINAL]:
    return {
      fields.NAME:name, 
      fields.WEIGHT:hsh[fields.WEIGHT], 
      fields.ARRAY: []
    }
  ar = []
  weight = hsh[fields.WEIGHT]
  for k,v in hsh.items():
    if not is_special(k):
      inner_hsh = to_a(v, k, sort_order, top)
      ar.append(inner_hsh)
  if sort_order == DESC_SORT:
    sign = -1
  else:
    sign = 1
  ar.sort(key=lambda elem: sign*elem[fields.WEIGHT])
  ar = ar[:top]
  return {
    fields.NAME: name,
    fields.WEIGHT: weight,
    fields.ARRAY: ar
  }

class Distribution:
  def __init__(self, save_lines):
    self.distrib = self.init()
    self.save_lines = save_lines

  def init(self):
    result = {
      fields.WEIGHT: 0,
      fields.LINES: [],
      fields.TERMINAL: True
    }
    return result

  def insert(self, values, match_data=None):
    hsh = self.distrib
    hsh[fields.WEIGHT] += 1
    if self.save_lines:
      hsh[fields.LINES].append(match_data)
    for v in values[:-1]:
      if not v in hsh:
        hsh[v] = self.init()
        hsh[fields.TERMINAL] = False
      hsh = hsh[v]
      hsh[fields.WEIGHT] += 1
      if self.save_lines:
        hsh[fields.LINES].append(match_data)
    if not values[-1] in hsh:
      hsh[values[-1]] = self.init()
      hsh[fields.TERMINAL] = False
    hsh = hsh[values[-1]]
    hsh[fields.WEIGHT] += 1
    if self.save_lines:
      hsh[fields.LINES].append(match_data)
    
  def empty(self):
    return self.distrib[fields.WEIGHT] == 0

class Aggregation:
  def __init__(self, params):
    default_params = {
      fields.NAME: '',
      fields.KEYS: [],
      fields.SORT_ORDER: DESC_SORT,
      fields.TOP: TOP,
      fields.EXCLUDE: {},
      fields.SAVE_LINES: False,
      fields.FILTER: {}
    }
    self.params = {}
    for k,v in default_params.items():
      self.params[k] = params[k] if k in params else v
    for f in default_params:
      if f in params:
        params.pop(f)
    self.params[fields.FILTER] = params
    self.distrib = Distribution(self.params[fields.SAVE_LINES])

  def insert(self, match_data):
    for key in self.params[fields.KEYS]:
      if key not in match_data:
        return
    for key in self.params[fields.EXCLUDE]:
      if key in match_data and match_data[key] == self.params[fields.EXCLUDE][key]:
        return
    for key in self.params[fields.FILTER]:
      if key not in match_data:
        return
      if self.params[fields.FILTER][key] != match_data[key]:
        return
    values = list(map(lambda x: match_data[x], self.params[fields.KEYS]))
    if self.params[fields.SAVE_LINES]:
      self.distrib.insert(values, match_data)
    else:
      self.distrib.insert(values)

  def get_distrib(self):
    hsh = to_a(
      self.distrib.distrib, 
      self.params[fields.NAME], 
      sort_order=self.params[fields.SORT_ORDER], 
      top=self.params[fields.TOP]
    )
    return hsh

  def empty(self):
    return self.distrib.empty()

class Counter:
  def __init__(self, params):
    self.name = params[fields.NAME]
    self.exclude = params[fields.EXCLUDE] if fields.EXCLUDE in params else {}
    for f in [fields.NAME, fields.EXCLUDE]:
      if f in params:
        params.pop(f)
    self.params = params
    self.cnt = 0

  def insert(self, match_data):
    for key in self.exclude:
      if key in match_data and match_data[key] == self.exclude[key]:
        return
    for key in self.params:
      if key not in match_data:
        return
      if self.params[key] != match_data[key]:
        return
    self.cnt += 1

  def get_counter(self):
    return {fields.NAME : self.name, fields.WEIGHT : self.cnt}