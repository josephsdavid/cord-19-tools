# COVID-19 Data Tools

Tools for making COVID 19 data slightly easier for everyone!

## Installation

```
pip install cord-19-tools
```

## The Paperset class

This is a class for lazily loading papers from the [CORD-19 dataset](https://pages.semanticscholar.org/coronavirus-research). Here are the instructions for use:

1. Download a dataset in tar.gz form from the **Download Here** section, or using [download bash script](data/download.sh) in this repository (which automatically completes step 2 for you)

2. Extract it into a directory of your choice (functionality for leaving the tarballs unpacked/online may be added later, this is version 0.0.1), for example:

```sh
tar -xvzf comm_use_subset.tar.gz 
```

3. Load it into python!

```python
import cotools
from pprint import pprint

# no `/` at the end please!
data = cotools.Paperset("data/comm_use_subset")

# indexes with ints
pprint(data[0])

# and slices!
pprint(data[:2])


print(len(data))

# takes about 5gb in memory
alldata = [x[0] for x in data]
```

Lets talk for a bit about how it works, and why it doesnt take a gigantic amount of memory. The files are not actually loaded into python ***until the data is indexed***. Upon indexing, the files at those indexes are read into python, resulting in a list of dictionaries.
