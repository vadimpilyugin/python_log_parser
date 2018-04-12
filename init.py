import parser as prs
import log_formats as fmt
import service as srv
import loader as ld
import aggregation as agg
import fields

import pprint
pp = pprint.PrettyPrinter(indent=2)

log_format_set = ld.load_log_formats(ld.content('log_formats.yml'))
service_set = ld.load_all_services('../../log_parser/services/templates')
p = prs.Parser(log_format_set, service_set)

a = agg.Aggregation(
  name="Распределение юзеров по ip",
  keys=["user_ip", "username"],
  top=30,
  sort_order='desc'
)

b = agg.Aggregation(
  name="Какие интересные имена подключались",
  keys=["username"],
  top=20,
  sort_order='asc'
)

c = agg.Aggregation(
  name="Какие сервисы не определены",
  keys=[fields.SERVICE],
  top=100,
  sort_order='desc'
)

d = agg.Aggregation(
  name="Для каких строк не нашлось шаблона",
  keys=[fields.SERVICE, fields.MESSAGE],
  top=10,
  sort_order='desc'
)

e = agg.Aggregation(
  name="Не нашлось формата",
  keys=[fields.FILENAME, fields.LOGLINE],
  top=100,
  sort_order='desc'
)

j = 0
errs = 0
for i in p.parse_dir('../../log_parser/logs1/vvv', files={}):
  if j % 5000 == 0:
    print(f"Parsed {j} lines, errors={errs}")
  if i[fields.ERRNO] != prs.OK:
    errs += 1
    match_data = i[fields.MATCH_DATA]
    if i[fields.ERRNO] == prs.NO_SERVICE:
      c.insert(match_data)
    elif i[fields.ERRNO] == prs.NO_TEMPLATE:
      # Нужно вставить поле MESSAGE обратно в MATCH_DATA
      match_data.update({fields.MESSAGE:i[fields.REASON]})
      d.insert(match_data)
    elif i[fields.ERRNO] == prs.NO_FORMAT:
      # Нужно вставить поле LOGLINE обратно в MATCH_DATA
      match_data.update({fields.LOGLINE:i[fields.REASON]})
      e.insert(match_data)
  else:
    a.insert(i[fields.MATCH_DATA])
    b.insert(i[fields.MATCH_DATA])
  j += 1

layout = {
  "All":[0,1,2,3,4]
}