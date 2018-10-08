# IN DEVELOPMENT


# import itertools as it
# from . import aggregation as agg
# from . import fields
# import numpy as np
# from collections import Counter
# import math

# class Periodicity:
#   def __init__(self, fields, k):
#     self.fields = fields
#     self.k = k
#     self.ar = []

#   def insert(self, elem):
#     self.ar.append(elem)

#   def thresh(self, x):
#     if x < 10:
#       return 1
#     elif x < 300:
#       return x*0.36
#     else:
#       return math.sqrt(39.234*x)

#   def eval(self, ar):
#     if len(ar) <= 4:
#       return None, None
#     a = []
#     i = 0
#     j = 1
#     while j < len(ar):
#       a.append(int((ar[j][fields.DATE] - ar[i][fields.DATE]).total_seconds()))
#       i += 1
#       j += 1
#     a = np.array(a)
#     mean, std = a.mean(), a.std()
#     score = mean / std if std > 1e-7 else 1e+7
#     if mean < 5 and len(a) < 10:
#       # бот
#       return None, None
#     if std < self.thresh(mean) or len(ar) < 10:
#       return mean, score
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
#       return mean, score

#   def walk_agg(self, distrib, keys, keys_values):
#     descr = {}
#     for i, value in enumerate(keys_values):
#       descr[keys[i]] = value
#     mean, score = self.eval(distrib[fields.LINES])
#     if mean is not None:
#       yield({
#         fields.PERIOD: mean,
#         fields.EVENT_TYPE: descr,
#         fields.VARIATION: 1/score,
#         # fields.LINES: distrib[fields.LINES],
#         fields.WEIGHT: distrib[fields.WEIGHT]
#       })
#     for d in distrib:
#       if not fields.is_special(d):
#         yield from self.walk_agg(distrib[d], keys, keys_values+(d,))

#   def calculate(self):
#     for keys in it.combinations(self.fields, self.k):
#       a = agg.Aggregation({
#         fields.KEYS: keys,
#         fields.NAME: 'Calculated Periodicity',
#         fields.SAVE_LINES: True
#       })
#       for i in self.ar:
#         a.insert(i)
#       yield from self.walk_agg(a.distrib.distrib, keys, tuple())