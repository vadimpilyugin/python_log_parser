import json
import pprint
import sys

def foo():
  pp = pprint.PrettyPrinter(indent=2)

  with open('log_parser/default.conf/api.json', 'r', encoding='utf-8') as f:
    content = json.loads(f.read())


  pp.pprint(content)
  for ep, value in content.items():
    args = value['params']
    if len(value['methods']) > 1:
      args.insert(0,'method')
    print("def "+value['handler']+"_ep("+(', '.join(args))+"):")
    print("  return None\n")
  
foo()