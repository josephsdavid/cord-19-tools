import cotools
from pprint import pprint

cotools.download(dir="data")

noncomm = cotools.Paperset("data/noncomm_use_subset")

data = cotools.Paperset("data/comm_use_subset")
pprint(data[0])
print(type(data[0]))
# dict

pprint(data[:2])
print(type(data[2:5]))
# list

print(len(data))

# takes about 5gb in memory
alldata = data[:]

len(data)

len(alldata)

