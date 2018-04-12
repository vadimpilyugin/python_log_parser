import init
import fields

NO_DISTRIB = "No distribution with that id"

def root_ep():
  return None

def distrib_ep(id):
  id = int(id)
  if id in init.agg.agg_hsh:
    a = init.agg.agg_hsh[id]
    hsh = a.get_distrib()
    print(hsh)
    hsh[fields.NAME] = a.name
    hsh[fields.KEYS] = a.keys
    return hsh
  else:
    return False, id, NO_DISTRIB

def counter_ep(id):
  return None

def layout_ep():
	return {
    "All" : [0,1,2,3,4]
  }

def server_ep(server):
  if server == "All":
    return [0,1,2,3,4]
  return None

def failed_services_ep():
  return not init.agg.agg_hsh[2].empty()

def failed_templates_ep():
  return not init.agg.agg_hsh[3].empty()

def failed_formats_ep():
  return not init.agg.agg_hsh[4].empty()