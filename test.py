from pprint import pprint

import cotools

# cotools.download(dir="data")

# noncomm = cotools.Paperset("data/noncomm_use_subset")

data = cotools.Paperset("data/custom_license")
# pprint(data[0])
# print(type(data[0]))

# get the text for one feature
cotools.text(data[0])

cotools.texts(data[:15])


# data.apply(len)

# dict

# pprint(data[:2])
print(type(data[2:5]))
# list

print(len(data))

# takes about 5gb in memory
# alldata = data[:]

# len(data)

# len(alldata)

txt = [["novel coronavirus"], ["ventilator", "cpap", "bipap"]]

x = cotools.search(data, txt)
print(len(x))
print(len(cotools.search(data, txt[0])))
print(len(cotools.search(data, txt[-1])))
