import json
import pprint
import sys

# s = input("Вы уверены? (Это перезапишет файл handlers.py): ")
# if s != "Y":
#   sys.exit(0)

pp = pprint.PrettyPrinter(indent=2)

with open('api.json') as f:
  content = json.loads(f.read())


pp.pprint(content)

# with open('handlers.py', 'w') as f:
for ep, value in content.items():
  args = value['params']
  if len(value['methods']) > 1:
    args.insert(0,'method')
  print(f"def {value['handler']+'_ep'}({', '.join(args)}):")
  print("  return None\n")