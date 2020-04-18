from pprint import pprint

import cotools

help(cotools.download)

cotools.download(dir="data", match = "2020-04-10", regex = True)


# noncomm = cotools.Paperset("data/noncomm_use_subset")

data = cotools.Paperset("data/noncomm_use_subset")

text(data[-1])


# pprint(data[0])
# print(type(data[0]))

# get the text for one feature
cotools.text(data[0])

cotools.texts(data[:15])


import pdb

pdb.set_trace()  # XXX BREAKPOINT
data.apply(len)


# dict

# pprint(data[:2])
print(type(data[2:5]))
# list

print(len(data))

# takes about 5gb in memory
# alldata = data[:]
import pdb; pdb.set_trace()  # XXX BREAKPOINT
#data[:]

# len(data)

# len(alldata)

txt = [["novel coronavirus"], ["ventilator", "cpap", "bipap"]]

import pdb

pdb.set_trace()  # XXX BREAKPOINT
x = cotools.search(data, txt)
print(len(x))
print(len(cotools.search(data, txt[0])))
print(len(cotools.search(data, txt[-1])))
