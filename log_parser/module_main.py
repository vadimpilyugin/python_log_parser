# import parser as prs
# import log_formats as fmt
# import service as srv
# import loader as ld
# import aggregation as agg
# import fields
# import time
# import itertools as it
# import distance
# import pprint
# from collections import defaultdict as dd
# import networkx as nx
# import re
# import json

# pp = pprint.PrettyPrinter(indent=2)

# id_mapper = {}

# def zero():
#   return 0

# def is_n_tandem(ar,i,n):
#   if i > len(ar):
#     return False
#   return ar[i:i+n] == ar[i+n:i+2*n]

# def tandem(ar,i,rng):
#   for n in rng:
#     if is_n_tandem(ar,i,n):
#       return n

# def simplify_ar(a):
#   if len(a) == 1:
#     return a
#   i = 0
#   f = False
#   while i < len(a)-1:
#     while i < len(a)-1 and a[i] == a[i+1]:
#       a[i] = -1
#       f = True
#       i += 1
#     if f:
#       a[i] += 10000
#       f = False
#     i += 1
#   return list(filter(lambda x: x > 0, a))

# def parse_file(write_to_file=True):
#   global pp
#   log_format_set = ld.load_log_formats(ld.content('log_formats.yml'))
#   service_set = ld.load_all_services('../../log_parser/services/templates')
#   p = prs.Parser(log_format_set, service_set, save_line=True, extract_date=True)
#   id_mapper = {}
#   ar = []
#   j = 0
#   errs = 0
#   start_time = time.time()
#   with open("input_data", "w") as f:
#     for i in p.parse_dir('../../log_parser/logs/sshd/', files={"sshd.log.2"}):
#       if j % 5000 == 0:
#         print(f"Parsed {j} lines, errors={errs}")
#       if i[fields.ERRNO] != prs.OK:
#         errs += 1
#         pp.pprint(i)
#       else:
#         templ_id = i[fields.MATCH_DATA][fields.TEMPLATE_ID]
#         msg = i[fields.MATCH_DATA][fields.MESSAGE]
#         if write_to_file:
#           f.write(f"{templ_id} # {msg}\n")
#         ar.append(templ_id)
#       j += 1
#   elapsed_time = time.time() - start_time
#   print(f"--- Elapsed time: {round(elapsed_time,2)}, lines per second: {j // elapsed_time}")
#   return ar

# def parse_to_json():
#   global pp
#   log_format_set = ld.load_log_formats(ld.content('log_formats.yml'))
#   service_set = ld.load_all_services('../../log_parser/services/templates')
#   p = prs.Parser(log_format_set, service_set, extract_date=False, save_line=True)
#   flds = ["user_ip", "username"]
#   j = 0
#   errs = 0
#   ar = []
#   for i in p.parse_dir('../../log_parser/logs/sshd', files={"sshd.log.3"}):
#     if j % 5000 == 0:
#       print(f"Parsed {j} lines, errors={errs}")
#     if i[fields.ERRNO] != prs.OK:
#       errs += 1
#       pp.pprint(i)
#     else:
#       try:
#         i = i[fields.MATCH_DATA]
#         for k in flds:
#           if k in i and i[k] is None:
#             i[k] = ''
#         ar.append({
#           fields.DATE:str(i[fields.DATE]),
#           fields.SERVICE:i[fields.SERVICE],
#           fields.MESSAGE:i[fields.MESSAGE],
#           fields.TEMPLATE_ID:i[fields.TEMPLATE_ID],
#           fields.LINEDATA:','.join([i[k] for k in flds if k in i])
#         })
#       except KeyError:
#         pp.pprint(i)
#       except TypeError:
#         pp.pprint(i)
#     j += 1
#   with open('input_data_sshd2.json','w') as f:
#     f.write(json.dumps(ar, indent=4, sort_keys=False, default=str))


# def read_file():
#   with open('input_data') as f:
#     return list(map(lambda x: eval(x), f.readlines()))

# def search_tandems(ar, rng=range(4,30)):
#   i = 0
#   hsh = dd(zero)
#   while i < len(ar):
#     size = tandem(ar, i, rng)
#     if size is not None:
#       # check if n-dem:
#       j = 1
#       while is_n_tandem(ar, i+j*size, size):
#         j += 1
#       # print(f'{i} -- {size} -- {ar[i:i+size]} -- {j+1}-кратный тандем!')
#       seq = tuple(ar[i:i+size])
#       hsh[seq] += j+1
#       i = i+j*size
#     else:
#       i += 1
#   return hsh

# def search_for_sequences(a, val):
#   i = 0
#   while i < len(a)-1:
#     if a[i] != val:
#       i += 1
#       continue
#     j = i
#     while i < len(a)-1 and a[i] == a[i+1]:
#       i+=1
#     if j != i:
#       yield(j,i+1)
#     i += 1

# def search_repeated_subseq(ar, max_shift = 50, min_seq = 4):
#   seqs = {}
#   if max_shift > len(ar):
#     max_shift = len(ar)
#   start = 1
#   while start < max_shift:
#     i = start
#     j = 0
#     sim = []
#     while i < len(ar):
#       sim.append(ar[i] == ar[j])
#       i += 1
#       j += 1
#     for left, right in search_for_sequences(sim, True):
#       if right - left >= min_seq:
#         seqs[tuple(ar[left:right])] = True
#     start += 1
#   return list(seqs.keys())

# def weight(ar,subseq):
#   ar = list(ar)
#   subseq = list(subseq)
#   return sum(ar[i:i+len(subseq)]==subseq for i in range(len(ar)))

# def weight_by_sim(ar, subseq, dist=2):
#   subseq = list(subseq)
#   return sum(distance.levenshtein(ar[i:i+len(subseq)], subseq) <= dist for i in range(len(ar)))

# # def split_and_remove_long_keys(hsh):
# #   keys_to_remove = dd(zero)
# #   keys_to_insert = dd(zero)
# #   print("------- Keys to remove -------")
# #   for k in hsh:
# #     tnd = search_tandems(k)
# #     if tnd:
# #       keys_to_remove[k] = True
# #       for i,j in tnd.items():
# #         keys_to_insert[i] += 2*j

# #   for k in keys_to_remove:
# #     hsh.pop(k)
# #   for k,v in keys_to_insert.items():
# #     if not k in hsh:
# #       print(f"New split key: {k}")
# #     print(f"Increased {hsh[k]} by {v}")
# #     hsh[k] += v

# def remove_repeats(hsh):
#   keys_to_insert = dd(zero)
#   for k in list(hsh.keys()):
#     res = search_repeated_subseq(k)
#     for kti in res:
#       # print(f"Key to insert: {kti}")
#       keys_to_insert[kti] += weight(k,kti)
#     if res:
#       hsh.pop(k)
#   for k in keys_to_insert:
#     hsh[k] += keys_to_insert[k]

# def remove_tandems(hsh, min_size=4, max_size=15):
#   keys_to_insert = dd(zero)
#   for k in list(hsh.keys()):
#     res = search_tandems(k, range(min_size, max_size))
#     for kti in res:
#       # print(f"Key to insert: {kti}")
#       keys_to_insert[kti] += hsh[k]*2
#     if res:
#       hsh.pop(k)
#   for k in keys_to_insert:
#     hsh[k] += keys_to_insert[k]

# def order_hsh(hsh):
#   ar = []
#   for k,v in hsh.items():
#     ar.append((k,v))
#   ar.sort(key=lambda x: -x[1])
#   return ar

# def k_to_str(k):
#   global id_mapper
#   return tuple(map(lambda x: id_mapper[x], k))

# def leven_mapper(keys):
#   already_in = set()
#   for k1 in keys:
#     if k1 not in already_in:
#       s = set()
#       s.add(k1)
#       for k2 in keys:
#         if k2 not in already_in and distance.levenshtein(k1, k2) <= 4:
#           s.add(k2)
#           already_in.add(k2)
#       yield(s)

# def cyclic_equiv(u, v):
#   n, i, j = len(u), 0, 0
#   if n != len(v):
#       return False
#   while i < n and j < n:
#       k = 1
#       while k <= n and u[(i + k) % n] == v[(j + k) % n]:
#           k += 1
#       if k > n:
#           return True
#       if u[(i + k) % n] > v[(j + k) % n]:
#           i += k
#       else:
#           j += k
#   return False

# def cyclic_levenstein_dist(k1,k2):
#   i = 0
#   m = None
#   while i < len(k1):
#     new_k1 = k1[i:]+k1[0:i]
#     dist = distance.levenshtein(new_k1, k2)
#     if m is None or dist < m:
#       m = dist
#     i += 1
#   return m

# def cyclic_levenstein_equiv(k1,k2,dist=1):
#   i = 0
#   while i < len(k1):
#     new_k1 = k1[i:]+k1[0:i]
#     if distance.levenshtein(new_k1, k2) <= dist:
#       return True
#     i += 1
#   return False

# def rotation_mapper(keys):
#   already_in = set()
#   for k1 in keys:
#     if k1 not in already_in:
#       s = set()
#       s.add(k1)
#       already_in.add(k1)
#       for k2 in keys:
#         if k2 not in already_in and cyclic_equiv(k1,k2):
#           s.add(k2)
#           already_in.add(k2)
#       yield(s)

# def combine_keys(hsh, keys):
#   for k in list(keys)[:-1]:
#     hsh.pop(k)

# def filter_for_tandems(keys, min_size=4, max_size=15):
#   for k in keys:
#     hsh = search_tandems(k, range(min_size, max_size))
#     if hsh:
#       # print(f"--- Key: {k}")
#       for k1 in hsh:
#         # print(f"+++ {k1}")
#         yield k1
#     else:
#       yield(k)

# def filter_for_repeats(keys):
#   for k in keys:
#     seq = search_repeated_subseq(k)
#     if seq:
#       for k1 in seq:
#         yield k1
#     else:
#       yield k

# def filter_for_rotations(keys):
#   already_in = set()
#   for k1 in keys:
#     if k1 not in already_in:
#       # print(f"--- Key {k1}")
#       already_in.add(k1)
#       for k2 in keys:
#         if k2 not in already_in and cyclic_equiv(k1,k2):
#           # print(f"+++ {k2}")
#           already_in.add(k2)
#       yield(k1)

# def group_by_similarity(keys, dist=2):
#   already_in = set()
#   for k1 in keys:
#     if k1 not in already_in:
#       already_in.add(k1)
#       s = set()
#       s.add(k1)
#       for k2 in keys:
#         if k2 not in already_in and cyclic_levenstein_dist(k1, k2) <= dist:
#           already_in.add(k2)
#           s.add(k2)
#       yield(s)

# def filter_for_identity(keys):
#   s = set()
#   for k in keys:
#     s.add(k)
#   for k in s:
#     yield(k)

# def max_key_in_group(s, ar):
#   m = None
#   mk = None
#   for k in s:
#     w = weight(ar, k)
#     if m is None or w > m:
#       m = w
#       mk = k
#   return (mk,m)

# def filter_for_similarity(keys, ar, dist=2):
#   for s in group_by_similarity(keys, dist):
#     k,v = max_key_in_group(s, ar)
#     yield(k)

# def combined_filter(keys):
#   print("=-------------- Combined filter --------------=")
#   # keys = list(filter_for_tandems(keys))
#   # print(len(keys))
#   # keys = list(filter_for_repeats(keys))
#   # print(len(keys))
#   keys = list(filter_for_rotations(keys))
#   print(len(keys))
#   keys = list(filter_for_identity(keys))
#   print(len(keys))
#   return keys

# def regex_from_key(key):
#   m = map(
#     lambda x:f"(?:{x-10000}.*\n)+" if x > 10000 else f"{x}.*\n", 
#     key
#   )
#   m = "".join(list(m))
#   return m

# def regex_from_set(s):
#   return '('+"|".join(map(lambda x: regex_from_key(x), s))+')'

# def network_from_keys(keys, ar):
#   keys = list(keys)
#   g = nx.Graph()
#   i = 0
#   j = 1
#   g.add_nodes_from(keys)
#   while i < len(keys)-1:
#     while j < len(keys):
#       if cyclic_levenstein_dist(keys[i], keys[j]) == 1:
#         g.add_edge(keys[i], keys[j])
#       j+=1
#     i += 1
#     j = i+1
#   return g

# def find_keys_by_chains(ar1, thresh = 100):
#   hsh = {}
#   for i in range(0,len(ar1)-1):
#     j = i+1
#     edge = (ar1[i],ar1[j])
#     try:
#       assert(ar1[i] != ar1[j])
#     except AssertionError:
#       print(ar1[i], ar1[j], i, j)
#       raise
#     if not edge in hsh:
#       hsh[edge] = 0
#     hsh[edge] += 1

#   keys_to_remove = {}
#   for k,v in hsh.items():
#     if v < thresh:
#       keys_to_remove[k] = True
#   for k in keys_to_remove:
#     hsh.pop(k)
#     # print("Popped", k)

#   print("\nОсталось ребер:", len(hsh),"\n")

#   strings = {}
#   string = ()
#   for i in range(0,len(ar1)-1):
#     j = i+1
#     edge = (ar1[i],ar1[j])
#     if not edge in hsh:
#       if not string in strings:
#         strings[string] = 0
#       strings[string] += 1
#       string = ()
#     else:
#       if not string:
#         string = edge
#       else:
#         string += (edge[1],)

#   strings.pop(tuple())
#   return strings.keys()

# def filter_rotate_to_start(keys, start):
#   for k in keys:
#     if start in k:
#       i = k.index(start)
#       yield(k[i:]+k[:i])
#     else:
#       yield(k)

# def filter_keys_by_stop(keys, stop=110000):
#   for k in keys:
#     if stop in k:
#       for i,j in it.groupby(k, lambda x: x == stop):
#         if not i:
#           yield(tuple(j))
#     else:
#       yield(k)

# def filter_keys_by_size(keys, min_size=2, max_size=30):
#   for k in keys:
#     if len(k) >= min_size and len(k) <= max_size:
#       yield(k)

# # def filter_key_expander(keys, start=10000):
# #   for k in keys:
# #     new_k = list()
# #     for i in k:
# #       if i > start:
# #         n_times = i // start;
# #         new_k.append()

# def procedure():
#   MAX_KEY_SIZE = 15
#   MIN_KEY_SIZE = 4
#   DIST = 2
#   parse_file(True)
#   ar = simplify_ar(read_file())
#   keys = list(filter_for_tandems((ar,), MIN_KEY_SIZE, MAX_KEY_SIZE))
#   keys = list(filter_rotate_to_start(keys, 375))
#   print(f"Keys1: {len(keys)}")
#   # keys = list(filter_for_tandems(keys))
#   keys = list(filter_for_rotations(keys))
#   keys = list(filter_for_identity(keys))
#   res = []
#   for s in group_by_similarity(keys, dist=DIST):
#     print('#####')
#     for s1 in s:
#       print(f"--- Key in set: {s1}")
#     k,v = max_key_in_group(s,ar)
#     s_reg = regex_from_set(s)
#     res.append((k,v,s_reg))
#     # res.append((k,v,regex_from_key(k).__repr__()))
#   res.sort(key=lambda x: -x[1])
#   for k,v,s in res:
#     print(f"+++ {v}!")
#     print(f"--- Regex:", s.__repr__())

# if __name__ == '__main__':

  
#   procedure()
#   # parse_to_json()

#   # parse_file(True)
#   # ar = simplify_ar(read_file())
#   # keys = list(filter_for_tandems((ar,)))
#   # keys = list(filter_keys_by_stop(keys))
#   # print(f"Keys1: {len(keys)}")
#   # keys = list(filter_rotate_to_start(keys, 498))
#   # for i in range(0,1):
#   #   keys = combined_filter(keys)
#   # keys = list(filter_rotate_to_start(keys, 498))
#   # keys = list(filter_keys_by_size(keys))
#   # keys2 = search_repeated_subseq(ar, min_seq=4)
#   # print(f"Keys2: {len(keys2)}")
#   # keys3 = list(find_keys_by_chains(ar, thresh=100))
#   # print(f"Keys3: {len(keys3)}")
#   # keys = keys+keys2+keys3
#   # print("----------")
#   # keys = list(filter_for_rotations(keys))
#   # keys = list(filter_for_identity(keys))
#   # # for i in keys:
#   # print(f"After rotation: {len(keys)}")
#   # print("----------")
#   # keys = list(filter_for_tandems(keys))
#   # keys = list(filter_for_identity(keys))
#   # # for i in keys:
#   # print(f"After tandems: {len(keys)}")
#   # print("----------")
#   # keys = list(filter_for_repeats(keys))
#   # keys = list(filter_for_identity(keys))
#   # for i in keys:
#   #   print(f"After repeats: {i}")
#   # print("----------")

#   # g = network_from_keys(keys, ar)

#   # Results
#   # res = []
#   # for s in group_by_similarity(keys, dist=4):
#   #   print('.')
#   #   k,v = max_key_in_group(s,ar)
#   #   res.append(k) #((k,v,regex_from_key(k).__repr__()))

#   # print("----------- Similarity Filter -------------")
#   # for i in range(0,4):
#   #   keys = list(filter_for_similarity(keys, ar, dist=2))
#   #   print(len(keys))
    
#   # res2 = []
#   # for s in group_by_similarity(keys, dist=4):
#   #   print('#####')
#   #   for s1 in s:
#   #     print(f"--- Key in set: {s1}")
#   #   k,v = max_key_in_group(s,ar)
#   #   s_reg = regex_from_set(s)
#   #   res2.append((k,v,s_reg))
#   #   # res2.append((k,v,regex_from_key(k).__repr__()))
#   # res2.sort(key=lambda x: -x[1])
#   # for k,v,s in res2:
#   #   print(f"+++ {v}!")
#   #   print(f"--- Regex:", s.__repr__())


#   # hsh = dd(zero)
#   # for k in keys:
#   #   hsh[k] = weight(ar, k)
#   # keys = list(group_by_similarity(keys))
#   # for i in keys:
#   #   print(f"After similarity: {i}")
#   # keys = list(filter_for_rotations())
#   # print(len(keys))
#   # hsh = dd(zero)
#   # hsh = search_tandems(ar)
#   # keys = list(hsh.keys())
#   # for s in rotation_mapper(keys):
#   #   combine_keys(hsh, s)
#   # remove_tandems(hsh)
#   # remove_repeats(hsh)
#   # keys = list(hsh.keys())
#   # for s in rotation_mapper(keys):
#   #   combine_keys(hsh, s)
#   # keys = list(hsh.keys())
  
#   # for s in leven_mapper(keys):
#   #   print(s)
#   #   combine_keys(hsh, s)


#   # print("============")
#   # res = order_hsh(hsh)
#   # pp.pprint(res[:20])

#   # print([i for i in hsh.keys()])

#   # keys = [i for i in hsh.keys()]

#   # dist = [[distance.levenshtein(i,j) for j in keys] for i in keys]
#   # pp.pprint(dist)

#   # repl = [''.join(i) for i in it.product('AGCT','AGCT','AGCT')]
#   # j = 0
#   # for key in hsh:
#   #   try:
#   #     hsh[key] = 'A'+repl[j]
#   #     j += 1
#   #   except IndexError:
#   #     print(j)

#   # for k,v in hsh.items():
#   #   print(f"{k} --> {v}")

#   # new_ar = list(map(lambda x: hsh[x], ar))
#   # print(ar[:20])
#   # print(new_ar[:20])

#   # with open('myseq','w') as f:
#   #   f.write(">myseq\n")
#   #   j = 0
#   #   for i in new_ar:
#   #     f.write(i)
#   #     j += 1
#   #     if j % 10 == 0:
#   #       f.write("\n")
