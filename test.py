import cotools
from pprint import pprint

noncomm = cotools.Paperset("data/noncomm_use_subset")

data = cotools.Paperset("data/comm_use_subset")
pprint(data[0])
pprint(data[:2])

print(len(data))

# takes about 5gb in memory
alldata = [x[0] for x in data]

