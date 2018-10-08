# IN DEVELOPMENT


# import fields as fld
# import numpy as np
# import itertools as it
# import aggregation as agg
# import math
# from collections import Counter

# class Periodicity:
#   def __init__(self, fn, k=2):
#     self.fn = fn
#     self.ar = []
#     self.keys = {}
#     self.k = k
#   def indert(self, elem):
#     self.ar.append(elem)
#     self.keys.update(elem)
#   def eval(self, ar):
#     if len(ar) <= 4:
#       return None
#     a = []
#     i = 0
#     j = 1
#     while j < len(ar):
#       a.append(int((ar[j][fld.DATE] - ar[i][fld.DATE]).total_seconds()))
#       i += 1
#       j += 1
#     a = np.array(a)
#     mean, std = a.mean(), a.std()
#     score = mean / std if std > 1e-7 else 1e+7
#     if mean < 5 and len(a) < 10:
#       # бот
#       return None
#     if std < self.thresh(mean) or len(ar) < 10:
#       return mean, std, score, len(a)+1
#     else:
#       a[a == 0] = 1
#       c = Counter(a).most_common(2)
#       mn = min(c[0][0],c[1][0])
#       mx = max(c[0][0],c[1][0])
#       t = 15
#       mn_val = min(c[0][1],c[1][1])
#       if mn_val > 10 and mx-mn > t:
#         a = a[a > mn+(mx-mn)/2]
#         mean, std = a.mean(), a.std()
#         score = mean / std if std > 1e-7 else 1e+7
#       return mean, std, score, len(a)+1
        
#       # if c[0][1] >= 4 and c[1][1] >= 4 and mx-mn > t:
#   def thresh(self, x):
#     if x < 10:
#       return 1
#     elif x < 300:
#       return x*0.36
#     else:
#       return math.sqrt(39.234*x)
#   def calculate(self):
#     ar = []
#     for key in [fld.DATE, fld.SERVER, fld.TEMPLATE_REGEX, fld.MESSAGE, fld.FILENAME, 'user_port','pid']:
#       if key in self.keys:
#         self.keys.pop(key)
#     # for keys in it.combinations(self.keys, self.k):
#     #   a = agg.Aggregation(keys=keys, save_lines=True)
#     #   for elem in self.ar:
#     #     a.insert(elem)
      

#     pts = []
#     for k in range(1,self.k+1):
#       for keys in it.combinations(self.keys, k):
#         a = agg.AggregationContainer(keys=keys)
#         for elem in self.ar:
#           a.insert(elem)
#         for keys in a.distrib:
#           skip = False
#           for skip_keys in pts:
#             if skip_keys == keys[:len(skip_keys)]:
#               skip = True
#           if skip:
#             continue
#           res = self.eval(a.distrib[keys])
#           if res is not None and res[1] < self.thresh(res[0]):
#             ar.append((keys, (round(res[0],1),round(res[2],1),res[3])))
#             pts.append(keys)
#     ar.sort(key=lambda elem: -elem[1][1])
#     # ar.sort(key=lambda elem: -elem[1][0])
#     return ar