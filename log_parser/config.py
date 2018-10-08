import yaml
import sys

default_config = {
  'log_folder': '/var/log',
  'report_file': 'report.yml',
  'templates': 'templates',
  'log_formats': 'log_formats.yml',
  'api_file': 'api.json'
}

def file_content_ok(content, default_config=default_config):
  success = True
  for k in default_config:
    if not k in content:
      print(k,"is missing in config.yml")
      success = False
  for k in content:
    if not k in default_config:
      print(k,"is an extra key")
      success = False
  return success

def create_new_config(filename='config.yml', content=default_config):
  with open(filename, 'w', encoding='utf-8') as f:
    f.write(yaml.dump(content, default_flow_style=False))

def pexit():
  print("Program exited.")
  sys.exit(1)

f = None
try:
  f = open('config.yml', 'r', encoding='utf-8')
except FileNotFoundError:
  s = input("config.yml does not exist in current directory. Create one? (Y/n): ")
  if s.lower() == 'y':
    create_new_config()
  else:
    pexit()
config = yaml.load(f)
f.close()
if not file_content_ok(config, default_config):
  pexit()