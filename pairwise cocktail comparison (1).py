#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np
import itertools
#import cockatoo

"""
n = 12
labels = range(n)
ser = pd.Series(np.random.randn(n), index=labels)
arr = ser.values
print(arr)


# In[19]:


m = [2,4,6,8,10,12]
ser1 = np.ndarray(m)


# In[23]:


arr = arr[:, None] - arr
df2 = pd.DataFrame(arr, labels, labels).abs()


# In[14]:


print(df2)


# In[5]:


from itertools import tee
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


# In[19]:


import json

file1 = open("/Users/kaileyferger/Downloads/C0160.json", "r")
file2 = open("/Users/kaileyferger/Downloads/C0163.json", "r")
cocktail1, cocktail2 = json.load(file1), json.load(file2)
#a = [cocktail1, cocktail2]
a = [1,2,3,4,5,6,7,8,9,10,11,12]
labels = range(len(a))
for v, w in pairwise(a):
    #ck1 = cockatoo.screen.parse_cocktail(v)
    #ck2 = cockatoo.screen.parse_cocktail(w)
    #cocktail_distance = cockatoo.metric.distance(ck1, ck2, weights=None)
    print(v,w)
    


# In[22]:
"""

from itertools import repeat, combinations

mylist = [1,2,3,4,5,6,7,8,9,10,11,12]
d = [[] for i in repeat(None, len(mylist))]
d[0].append(0)
d[-1].append(0)
#empty_array = pd.DataFrame(index=mylist, columns=mylist)

for a, b in itertools.combinations(mylist, 2):
    #print("{}:{}".format(mylist.index(a),(a-1)))
    index = mylist.index(a)
    diff = a*b
    d[index].append(diff)
#print(empty_array)

for l in d:
    if len(l) < len(mylist):
        len_diff = len(mylist) - len(l)
        for i in range(len_diff):
            l.insert(i,0)

df = pd.DataFrame(d, index=mylist, columns = mylist)
df[mylist] = df[mylist].replace({0:np.nan, 0:np.nan})
print(df)


# In[ ]:




