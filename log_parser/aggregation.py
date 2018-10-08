from . import fields

ASC = 'asc'
DESC = 'desc'
TOP = 10

class Report:
  def __init__(self):
    self.servers = {}
  def add_stat(self, server, stat_type, stat):
    if server not in self.servers:
      self.servers[server] = {
        fields.COUNTERS: [],
        fields.DISTRIBUTION: []
      }
    self.servers[server][stat_type].append(stat)



# def to_a(hsh, name, sort_order, sort_type, top):
#   if hsh[fields.TERMINAL]:
#     return {
#       fields.NAME:name, 
#       fields.WEIGHT:hsh[fields.WEIGHT], 
#       fields.ARRAY: [],
#       fields.DISTINCT: hsh[fields.DISTINCT]
#     }
#   ar = []
#   weight = hsh[fields.WEIGHT]
#   for k,v in hsh.items():
#     if not fields.is_special(k):
#       inner_hsh = to_a(v, k, sort_order, sort_type, top)
#       ar.append(inner_hsh)
#   if sort_order == DESC:
#     sign = -1
#   else:
#     sign = 1
#   ar.sort(key=lambda elem: sign*elem[fields.WEIGHT if sort_type == WEIGHT else fields.DISTINCT])
#   ar = ar[:top]
#   return {
#     fields.NAME: name,
#     fields.WEIGHT: weight,
#     fields.ARRAY: ar,
#     fields.DISTINCT: hsh[fields.DISTINCT]
#   }

class TrieNode:
  def __init__(self, value):
    self.children = dict()
    self.value = value
    self.saved_lines = []
    self.weight = 0
  def __repr__(self):
    return f"[{self.value} w:{self.weight} d:{len(self.children)} l={len(self.saved_lines)}]"
  def __getitem__(self, key):
    return self.children[key]

class Trie:
  def __init__(self, save_lines=False):
    self.root = TrieNode(None)
    self.save_lines = save_lines

  def insert(self, key, line=None):
    curr_node = self.root
    curr_node.weight = curr_node.weight + 1
    for item in key:
      if not item in curr_node.children:
        curr_node.children[item] = TrieNode(item)
      curr_node = curr_node.children[item]
      curr_node.weight = curr_node.weight + 1
    if self.save_lines:
      assert line is not None, "No line to save!"
      curr_node.saved_lines.append(line)

  def preorder(self, root, depth=0):
    s = f"{root}{depth} "
    for k,child_root in root.children.items():
      s = s + self.preorder(child_root, depth+1)
    return s

  def __repr__(self):
    return self.preorder(self.root)

  def clear(self):
    self.root = TrieNode()

  def empty(self):
    return len(self.root.children) == 0

  def to_a(self, root, name=None, sort_order=DESC, sort_field=fields.WEIGHT, top=TOP):
    node = {
      fields.NAME:root.value, 
      fields.WEIGHT:root.weight, 
      fields.DISTINCT: len(root.children),
      fields.ARRAY: []
    }
    n_elems = 0
    for value, child_root in root.children.items():
      node[fields.ARRAY].append(self.to_a(child_root, None, sort_order, sort_field, top))
      n_elems += 1
      if (n_elems >= top):
        break
    if sort_order == DESC:
      sign = -1
    else:
      sign = 1
    node[fields.ARRAY].sort(key=lambda x: sign * x[sort_field])
    if name:
      node[fields.NAME] = name
    return node

# t = Trie(save_lines=False)
# t.insert("doc")
# t.insert("dox")
# t.insert("dot")
# t.insert("dr")
# t.insert("eu")
# t.insert("c")
# t

# class Distribution:
#   def __init__(self, save_lines):
#     self.distrib = self.init()
#     self.save_lines = save_lines

#   def init(self):
#     result = {
#       fields.WEIGHT: 0,
#       fields.DISTINCT: 0,
#       fields.LINES: [],
#       fields.TERMINAL: True
#     }
#     return result

#   def insert(self, values, match_data=None):
#     hsh = self.distrib
#     hsh[fields.WEIGHT] += 1
#     if self.save_lines:
#       hsh[fields.LINES].append(match_data)
#     for v in values[:-1]:
#       if not v in hsh:
#         hsh[v] = self.init()
#         hsh[fields.TERMINAL] = False
#         hsh[fields.DISTINCT] += 1
#       hsh = hsh[v]
#       hsh[fields.WEIGHT] += 1
#       if self.save_lines:
#         hsh[fields.LINES].append(match_data)
#     if not values[-1] in hsh:
#       hsh[values[-1]] = self.init()
#       hsh[fields.TERMINAL] = False
#       hsh[fields.DISTINCT] += 1
#     hsh = hsh[values[-1]]
#     hsh[fields.WEIGHT] += 1
#     hsh[fields.DISTINCT] = 1
#     if self.save_lines:
#       hsh[fields.LINES].append(match_data)
    
#   def empty(self):
#     return self.distrib[fields.WEIGHT] == 0

class Aggregation:
  default_params = {
    fields.NAME: '',
    fields.KEYS: [],
    fields.SORT_ORDER: DESC,
    fields.SORT_FIELD: fields.WEIGHT,
    fields.TOP: TOP,
    fields.EXCLUDE: {},
    fields.SAVE_LINES: False,
    fields.EQ: {}
  }

  def __init__(self, params):
    self.params = {}
    for k,v in Aggregation.default_params.items():
      self.params[k] = params[k] if k in params else v
    self.inner = Trie(self.params[fields.SAVE_LINES])

  def insert(self, match_data):
    for key in self.params[fields.EXCLUDE]:
      if key in match_data and match_data[key] == self.params[fields.EXCLUDE][key]:
        return
    for key in self.params[fields.EQ]:
      if key not in match_data:
        return
      if self.params[fields.EQ][key] != match_data[key]:
        return
    for key in self.params[fields.KEYS]:
      if key not in match_data:
        return

    values = list(map(lambda x: match_data[x], self.params[fields.KEYS]))
    if self.params[fields.SAVE_LINES]:
      self.inner.insert(values, match_data)
    else:
      self.inner.insert(values)

  def get_distrib(self):
    return self.inner.to_a(
      self.inner.root,
      self.params[fields.NAME],
      self.params[fields.SORT_ORDER],
      self.params[fields.SORT_FIELD],
      self.params[fields.TOP]
    )

  def empty(self):
    return self.inner.empty()

# class Aggregation:
#   default_params = {
#     fields.NAME: '',
#     fields.KEYS: [],
#     fields.SORT_ORDER: DESC,
#     fields.SORT_FIELD: WEIGHT,
#     fields.TOP: TOP,
#     fields.EXCLUDE: {},
#     fields.SAVE_LINES: False,
#     fields.EQ: {}
#   }

#   def __init__(self, params):
#     self.params = {}
#     for k,v in default_params.items():
#       self.params[k] = params[k] if k in params else v
#     self.distrib = Distribution(self.params[fields.SAVE_LINES])

#   def insert(self, match_data):
#     for key in self.params[fields.KEYS]:
#       if key not in match_data:
#         return
#     for key in self.params[fields.EXCLUDE]:
#       if key in match_data and match_data[key] == self.params[fields.EXCLUDE][key]:
#         return
#     for key in self.params[fields.EQ]:
#       if key not in match_data:
#         return
#       if self.params[fields.EQ][key] != match_data[key]:
#         return
#     values = list(map(lambda x: match_data[x], self.params[fields.KEYS]))
#     if self.params[fields.SAVE_LINES]:
#       self.distrib.insert(values, match_data)
#     else:
#       self.distrib.insert(values)

#   def get_distrib(self):
#     hsh = to_a(
#       self.distrib.distrib, 
#       self.params[fields.NAME], 
#       sort_order=self.params[fields.SORT_ORDER], 
#       sort_type=self.params[fields.SORT_FIELD],
#       top=self.params[fields.TOP]
#     )
#     hsh[fields.SORT_FIELD] = self.params[fields.SORT_FIELD]
#     return hsh

#   def empty(self):
#     return self.distrib.empty()

class Counter:
  default_params = {
    fields.NAME: '',
    fields.EXCLUDE: {},
    fields.EQ: {}
  }

  def __init__(self, params):
    self.params = {}
    for k,v in Counter.default_params.items():
      self.params[k] = params[k] if k in params else v
    self.cnt = 0

  def insert(self, match_data):
    for key in self.params[fields.EXCLUDE]:
      if key in match_data and match_data[key] == self.params[fields.EXCLUDE][key]:
        return
    for key in self.params[fields.EQ]:
      if key not in match_data:
        return
      if self.params[fields.EQ][key] != match_data[key]:
        return
      self.cnt += 1

  def get_counter(self):
    return {
      fields.NAME : self.name, 
      fields.WEIGHT : self.cnt
    }