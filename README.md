# COVID-19 Data Tools

Tools for making COVID 19 data slightly easier for everyone! If you A) think something would be useful in your research or B) have some helpful code to contribute, make an issue or PR ASAP so we can get your code shared!

## Installation

```
pip install cord-19-tools
```

## Downloading the data

To download and extract the data, use the `download` function:

```python
import cotools
from pprint import pprint

cotools.download(dir="data")
```

For now this just downloads the data from the [CORD-19 dataset](https://pages.semanticscholar.org/coronavirus-research), metadata is not included (will be by end of day), extracts all the tarfiles, and places them in a directory

## The Paperset class

This is a class for lazily loading papers from the [CORD-19 dataset](https://pages.semanticscholar.org/coronavirus-research).


```python

# no `/` at the end please!
data = cotools.Paperset("data/comm_use_subset")

# indexes with ints
pprint(data[0])
# returns a dict

# and slices!
pprint(data[:2])
# returns a list of dicts


print(len(data))

# takes about 5gb in memory
alldata = data[:]
```

Lets talk for a bit about how it works, and why it doesnt take a gigantic amount of memory. The files are not actually loaded into python ***until the data is indexed***. Upon indexing, the files at those indexes are read into python, resulting in a list of dictionaries. This means you can still contribute while working on a low resource system.


### Getting text and abstracts

For text, there is the `text` function, which returns the text from a single document, the `texts` function, which returns the text from multiple documents, and the `Paperset.texts()` function, which gets the text from all documents:

```python
print(cotools.text(data[0]))
print(cotools.texts(data[12:18]))

alltext = data.texts()
# alltext = cotools.texts(alldata)
```

For abstracts, we have a similar API:

```python
print(cotools.abstract(data[0]))
print(cotools.abstracts(data[12:18]))

allabs = data.abstracts()
# allabs = cotools.abstracts(alldata)
```

### Manipulating

You can also manipulate the documents with the `Paperset.apply` method:

```python
keys = comm_use.apply(lambda x: list(x.keys()))
# then lets combine them into a set
print(set(sum(keys, [])))
```

## Hopkins data

The Hopkins data can be loaded with `load_hopkins`. It loads three dicts, each containing data from the hopkins dataset:

```{python}
confirmed, deaths, recoverise = cotools.load_hopkins()
```

# TODO

- [ ] Metadata
- [ ] Other data, for example data from [this aggregate site](https://www.kiragoldner.com/covid19/) and [this google spreadsheet](https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vRwAqp96T9sYYq2-i7Tj0pvTf6XVHjDSMIKBdZHXiCGGdNC0ypEU9NbngS8mxea55JuCFuua1MUeOj5/pubhtml#)
