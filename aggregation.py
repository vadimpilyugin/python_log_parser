import fields

DESC_SORT = 'desc'
cnt = 0
agg_hsh = {}

def is_iterable(hsh):
  return hasattr(hsh, '__iter__')

def to_a(hsh, sort_order, top):
  global DESC_SORT
  if not is_iterable(hsh):
    return {fields.ARRAY:hsh, fields.WEIGHT:hsh}
  ar = []
  weight = hsh[fields.TOTAL]
  for k,v in hsh.items():
    if k != fields.TOTAL:
      inner_hsh = to_a(v, sort_order, top)
      ar.append((k, inner_hsh))
  if sort_order == DESC_SORT:
    sign = -1
  else:
    sign = 1
  ar.sort(key=lambda elem: sign*elem[1][fields.WEIGHT])
  ar = ar[:top]
  return {
    fields.ARRAY:list(
      map(
        lambda elem: [elem[0], elem[1][fields.ARRAY]], ar
      )
    ), 
    fields.WEIGHT:weight
  }

class Distribution:
  def __init__(self):
    self.distrib = self.init()

  def init(self):
    return {
      fields.TOTAL : 0,
      # fields.DISTINCT : 0,
    }

  def insert(self, values):
    hsh = self.distrib
    for v in values[:-1]:
      if not v in hsh:
        hsh[v] = self.init()
        # hsh[fields.DISTINCT] += 1
      hsh[fields.TOTAL] += 1
      hsh = hsh[v]
    if not values[-1] in hsh:
      hsh[values[-1]] = 0
      # hsh[fields.DISTINCT] += 1
    hsh[values[-1]] += 1
    hsh[fields.TOTAL] += 1

  def empty(self):
    return self.distrib[fields.TOTAL] == 0

class Aggregation:
  def __init__(self, name, keys, sort_order=DESC_SORT, top=10):
    global cnt
    global agg_hsh
    self.name = name
    self.keys = keys
    self.sort_order = sort_order
    self.top = top
    self.distrib = Distribution()
    self.id = cnt
    cnt += 1
    agg_hsh[self.id] = self

  def insert(self, match_data):
    for key in self.keys:
      if key not in match_data:
        return
    values = list(map(lambda x: match_data[x], self.keys))
    self.distrib.insert(values)

  def get_distrib(self):
    return to_a(self.distrib.distrib, sort_order=self.sort_order, top=self.top)

  def empty(self):
    return self.distrib.empty()