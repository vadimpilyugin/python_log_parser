import yaml
import os

def abs_path(path):
  if os.path.isabs(path):
    return path
  root_dir = os.path.dirname(__file__)
  return os.path.join(root_dir, path)

with open(abs_path('default.conf/config.yml'), 'r', encoding='utf-8') as f:
  config = yaml.load(f)
for k in config:
  config[k] = abs_path(config[k])