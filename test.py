import cotools
from pprint import pprint

data = cotools.Paperset("data/comm_use_subset")
pprint(data[0])
pprint(data[:2])
