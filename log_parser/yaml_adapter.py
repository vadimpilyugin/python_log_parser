# IN DEVELOPMENT


# import yaml
# import os

# class YamlAdapter:
#   def __init__(self, fn):
#     if not os.path.exists(fn):
#       with open(fn, 'w') as f:
#         f.write("---\n")
#     with open(fn, 'r') as f:
#       self.fn = fn
#       self.content = yaml.load(f)
#   def _traverse(self, keys):
#     hsh = self.content
#     for k in keys[:-1]:
#       if not k in hsh:
#         hsh[k] = {}
#       hsh = hsh[k]
#     return hsh
#   def _save(self):
#     with open(self.fn, 'w') as f:
#       f.write(yaml.dump(self.content,default_flow_style=False))
#   def append(self, keys, elem):
#     if not isinstance(keys, type(tuple())):
#       keys = (keys,)
#     hsh = self._traverse(keys)
#     hsh[keys[-1]].append(elem)
#     self._save()
#   def __getitem__(self, keys):
#     if not isinstance(keys, type(tuple())):
#       keys = (keys,)
#     hsh = self._traverse(keys)
#     return hsh[keys[-1]]
#   def __setitem__(self, keys, elem):
#     if not isinstance(keys, type(tuple())):
#       keys = (keys,)
#     hsh = self._traverse(keys)
#     hsh[keys[-1]] = elem
#     self._save()
#   def __iter__(self):
#     yield from self.content.__iter__()
#   def pop(self, keys, i):
#     hsh = self._traverse(keys)
#     hsh[keys[-1]].pop(i)
#     self._save()