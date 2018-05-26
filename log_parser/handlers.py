from . import parser as prs
from . import log_formats as fmt
from . import service as srv
from . import loader as ld
from . import aggregation as agg
from . import fields
from .config import config
import os
import pprint
import re

pp = pprint.PrettyPrinter(indent=2)

log_format_set = ld.load_log_formats(ld.content(config['log_formats']))
service_set = ld.load_all_services(config['templates'])
p = prs.Parser(log_format_set, service_set)

aggs = ld.load_aggregations()
err_services = agg.Aggregation({
  fields.NAME : "Какие сервисы не определены",
  fields.KEYS : [fields.SERVICE],
  fields.SAVE_LINES : True
})

err_templates = agg.Aggregation({
  fields.NAME : "Для каких строк не нашлось шаблона",
  fields.KEYS : [fields.SERVICE, fields.MESSAGE],
})

err_format = agg.Aggregation({
  fields.NAME : "Не нашлось формата",
  fields.KEYS : [fields.FILENAME, fields.LOGLINE],
})

# need_to_save = True
global_parse_stats = {}

def root_ep():
  return None
  
def layout_ep():
  servers = list(aggs.keys())
  servers.sort()
  if fields.ALL_SERVERS in aggs:
    servers.pop(servers.index(fields.ALL_SERVERS))
    servers.insert(0, fields.ALL_SERVERS)
  return list(map(
    lambda server: {
      fields.NAME : server,
      fields.COUNTERS : list(range(len(aggs[server][fields.COUNTERS]))) if fields.COUNTERS in aggs[server] else [],
      fields.DISTRIBUTIONS : list(range(len(aggs[server][fields.DISTRIBUTIONS]))) if fields.DISTRIBUTIONS in aggs[server] else [],
    },
    servers
  ))

def layout_distributions_ep(server):
  hsh = {
    fields.NAME: "Распределения",
    fields.WEIGHT: len(aggs[server][fields.DISTRIBUTIONS]),
    fields.ARRAY: []
  }
  if not fields.DISTRIBUTIONS in aggs[server]:
    return hsh
  for stat in aggs[server][fields.DISTRIBUTIONS]:
    hsh[fields.ARRAY].append(stat.get_distrib())
  return hsh

def layout_counters_ep(server):
  hsh = {
    fields.NAME: "Счетчики",
    fields.ARRAY: []
  }
  if not fields.COUNTERS in aggs[server]:
    return hsh
  for stat in aggs[server][fields.COUNTERS]:
    hsh[fields.ARRAY].append(stat.get_counter())
  return hsh

def layout_failed_ep():
  hsh = {
    fields.NAME: "Ошибки при парсинге",
    fields.WEIGHT: 0,
    fields.ARRAY: []
  }
  hsh[fields.ARRAY].append(err_services.get_distrib())
  if hsh[fields.ARRAY][-1][fields.WEIGHT] == 0:
    hsh[fields.ARRAY].pop()
  hsh[fields.ARRAY].append(err_templates.get_distrib())
  if hsh[fields.ARRAY][-1][fields.WEIGHT] == 0:
    hsh[fields.ARRAY].pop()
  hsh[fields.ARRAY].append(err_format.get_distrib())
  if hsh[fields.ARRAY][-1][fields.WEIGHT] == 0:
    hsh[fields.ARRAY].pop()
  hsh[fields.WEIGHT] = len(hsh[fields.ARRAY])
  return hsh

def server_ep(server):
  return aggs[server]

# def save_ep(method):
#   global need_to_save
#   if method == 'GET':
#     return need_to_save
#   else:
#     need_to_save = False
#     return True

def parse_single_ep(server, filename):
  if filename in global_parse_stats:
    return global_parse_stats[filename]
  with open(os.path.join(config['log_folder'], server, filename)) as f:
    s = {
      'ok' : 0,
      'fail' : 0
    }
    format_errors = 0
    MAX_FORMAT_ERRORS = 100
    for i in p.parsed_logline_stream(f):
      match_data = i[fields.MATCH_DATA]
      if i[fields.ERRNO] != prs.OK:
        s['fail'] += 1
        if i[fields.ERRNO] == prs.NO_SERVICE:
          err_services.insert(match_data)
        elif i[fields.ERRNO] == prs.NO_TEMPLATE:
          # match_data.update({fields.MESSAGE:i[fields.REASON]})
          err_templates.insert(match_data)
        elif i[fields.ERRNO] == prs.NO_FORMAT and format_errors < MAX_FORMAT_ERRORS:
          format_errors += 1
          i.update({fields.LOGLINE:i[fields.REASON], fields.FILENAME:filename})
          err_format.insert(i)
          # print('Current weight:', err_format.get_distrib()[fields.WEIGHT])
          # pp.pprint(i)
      else:
        s['ok'] += 1
        if match_data[fields.SERVER] in aggs:
          for _,v in aggs[match_data[fields.SERVER]].items():
            for stat in v:
              stat.insert(match_data)
        if fields.ALL_SERVERS in aggs:
          for _,v in aggs[fields.ALL_SERVERS].items():
            for stat in v:
              stat.insert(match_data)
  global_parse_stats[filename] = s
  return s



def logs_servers_ep():
  l = []
  for i in os.listdir(config['log_folder']):
    if os.path.isdir(os.path.join(config['log_folder'],i)):
      l.append(i)
  l.sort()
  return l

def logs_filenames_ep(server, filter_out=r'.*\.gz|.*\.tgz|.*\.zip'):
  l = []
  for i in os.listdir(os.path.join(config['log_folder'],server)):
    if not re.match(filter_out, i):
      l.append(i)
  l.sort()
  return l

def config_ep():
  return config