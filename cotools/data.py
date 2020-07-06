import json
import os

import gzip

import traceback
from datetime import datetime
from datetime import timedelta
import shutil
import tarfile
from functools import reduce, partial
from typing import Any, Callable, Dict, List, Sequence, TypeVar, Union, overload
from urllib.request import urlopen
import requests
import multiprocessing
import glob

import xmltodict as xml
import re

from .text import _get_abstract, _get_text

searchtext = Union[str, List[str]]
searchtexts = Union[searchtext, List[searchtext]]
textlist = List[Dict[str, Any]]
nestedlist = List[List[str]]


class Paperset:
    """
    The Paperset class:
        __init__ args:
            directory: a string, the directory where the jsons are stored

            description:
                lazy loader for cord-19 text files. Data is not actually loaded
                until indexing, until then it just indexes files. Can be
                indexed with both ints and slices.
    """

    def __init__(self, directory: str) -> None:
        self.directory = directory
        # get all of the text files recursively
        file_paths = glob.glob(self.directory + "/**/*.json", recursive=True)
        self.dir_dict = {idx: file_path for idx, file_path in enumerate(file_paths)}
        self.keys = list(self.dir_dict.keys())

    def _load_file(self, path: str) -> dict:
        with open(f"{path}") as handle:
            outdict = json.loads(handle.read())
        return outdict

    def __getitem__(self, indices: Union[int, slice]) -> Union[list, dict]:
        slicedkeys = list(self.dir_dict.keys())[indices]
        if not isinstance(slicedkeys, list):
            slicedkeys = [slicedkeys]
        out = [self._load_file(self.dir_dict[key]) for key in slicedkeys]
        if len(out) == 1:
            return out[0]
        else:
            return out

    def _helper(self, k: int, fun: Callable[..., Any]) -> Any:
        return fun(self._load_file(self.dir_dict[k]))

    def apply(self, fn: Callable[..., Any]) -> List[Any]:
        """
        Paperset.apply:
            Iterate a function through a paperset
        ---------------------------------------------
        args:
            fn: any function! Should work on the structure of paperset[0]

        runs in parallel!
        """
        helper = partial(self._helper, fun=fn)
        with multiprocessing.Pool(None) as p:
            res = p.map(helper, self.dir_dict.keys())
        return list(res)
        # return [fn(self._load_file(self.dir_dict[k])) for k in self.dir_dict.keys()]

    def texts(self) -> List[str]:
        """
        Papeset.texts:
            get all the text of all the papers, in list form!
        """
        return self.apply(_get_text)

    def abstracts(self) -> List[str]:
        """
        Papeset.abstracts:
            get all the abstracts of all the papers, in list form!
        """
        return self.apply(_get_abstract)

    def __len__(self) -> int:
        return len(self.dir_dict.keys())


def _search_helper(x: dict, txt: List[str]) -> bool:
    if any(c in _get_text(x).lower() for c in txt) or any(
        c in _get_abstract(x).lower() for c in txt
    ):
        return x
    else:
        return None


def _search(ps: Union[Paperset, textlist], txt: Any) -> textlist:
    # some checkers on txt, to prevent weirdness
    if type(txt[0]) is list:
        raise ValueError("Items of the search cannot be nested lists!")
    if type(txt) is str:
        txt = [txt]

    # If we accept a paperset, which has thousands of papers, we want to operate
    # in parallel
    if type(ps) is Paperset:
        # load the text into the helper function
        helper = partial(_search_helper, txt=txt)
        # apply in parallel!
        out = ps.apply(helper)
        return list(filter(lambda x: x is not None, out))
    else:
        return [
            x
            for x in ps
            if any(c in _get_text(x).lower() for c in txt)
            or any(c in _get_abstract(x).lower() for c in txt)
        ]


def search(
    ps: Union[Paperset, textlist], terms: Union[searchtexts, searchtext, nestedlist],
) -> textlist:
    """
    search:
        search through a paperset or list of paper dicts
    -----------------------------------------------------
    args:
        ps: a paperset or list of paper dicts
        terms: search terms, a list or nested (one layer of nesting only) list
    -----------------------------------------------------
    how it works:
        search(ps, ['string']) will search for all papers containing the phrase
        'string'
        search(ps, ['string1', 'string2']) will search for all papers containing
        either phrase
        search(ps, [['string1'], ['string2']]) will search for all papers
        containing both phrases
        search(ps, [['string1', 'string2'], ['string3', 'string4']]) will
        search for all papers containing both (either string1 or string 2) and
        (either string3 or string4)
    ----------------------------------------------------
    notes:
        search(ps, [['string1']]) will return weird results! Do not do!
        you do not have to worry about case! That is taken care of!

    """
    if type(terms) is not list:
        raise ValueError("search terms must be a list!!")
    types = [type(x) for x in terms]
    nests = len(list(filter(lambda x: x is list, types)))
    if nests != 0:
        return reduce(lambda x, y: _search(x, y), terms, ps)
    else:
        return _search(ps, terms)


def download(
    dir: str = ".", match: str = ".tar.gz", regex: bool = False, metadata: bool = True
) -> None:
    """
    download:
        Download CORD-19 dataset from ai2's S3 bucket.
    -----------------------------------------------------
    args:
        dir:    Directory to download the data into.
        match:  A string dictating which files to download. Defaults to match
                all tar files.
        regex:  If regex should be used. Otherwise, a `match in x` is used.
        metadata: Should metadata be downloaded. Defaults to True
    -----------------------------------------------------
    how it works:
        Match all files:                `download('data', match='*')`
        Match only JSON files:          `download('data', match='.json')`
        Match tar files from April 10:  `download('data', match='2020-04-10.*.tar.gz', regex=True)`
    """

    s3bucket_url = "https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"
    site = xml.parse(requests.get(s3bucket_url).content)["ListBucketResult"]["Contents"]

    def file_filter(f: str) -> bool:
        if regex:
            return re.search(match, f)
        return not match or (match in f) or (match == "*")

    keys = list(filter(file_filter, (x["Key"] for x in site)))
    if metadata:
        md = list(filter(re.compile("metadata").search, [x["Key"] for x in site]))
        dates = [datetime.strptime(x.split("/")[0], "%Y-%m-%d") for x in md]
        latest_metadata = md[dates.index(max(dates))]
        keys += [latest_metadata]
        mag_md = list(
            filter(
                re.compile("metadata_with_mag_mapping").search, [x["Key"] for x in site]
            )
        )
        dates = [datetime.strptime(x.split("/")[0], "%Y-%m-%d") for x in mag_md]
        latest_metadata_mappings = mag_md[dates.index(max(dates))]
        keys += [latest_metadata_mappings]
    data = dict(((os.path.basename(k), os.path.join(s3bucket_url, k)) for k in keys))
    assert data, "No files matched."
    if not os.path.exists(dir):
        os.mkdir(dir)
    
    for fp, url in data.items():
        try:
            res = requests.get(url, stream=True)
            
            if res.status_code != 200:
                print(f"Failed to download {url}: Got status {res.status_code}")
                continue
            
            print(f"Processing {url} ... ", end="")
            if fp.endswith(".tar.gz"):
                shutil.rmtree(
                    os.path.join(dir, fp.replace(".tar.gz", "")), ignore_errors=True
                )
                try:
                    tar = tarfile.open(fileobj=res.raw, mode="r|gz")
                    tar.extractall(dir)
                except Exception as e:
                    if type(e) == tarfile.ReadError:
                        # quick fix for arxiv.org package
                        # background: https://arxiv.org/help/faq/browsergunzip + https://github.com/psf/requests/issues/4346
                        res.close()
                        import urllib.request
                        urllib.request.urlretrieve(url, os.path.join(dir, fp))
                        shutil.unpack_archive(os.path.join(dir, fp), os.path.join(dir, fp.replace(".tar.gz", "")),"tar")
                        os.remove(os.path.join(dir, fp))
                    else:
                        raise       
            else:
                with open(os.path.join(dir, fp), "wb") as f:
                    f.write(res.content)
            print("Done.")
        except Exception as e:
            print(f"Failed:", e)
            traceback.print_tb(e.__traceback__)

            
            


def last_friday() -> str:
    target_dayofweek = 4  # Friday
    current_dayofweek = datetime.now().weekday()  # Today
    if target_dayofweek <= current_dayofweek:
        # target is in the current week
        endDate = datetime.now() - timedelta(current_dayofweek - target_dayofweek)
    else:
        # target is in the previous week
        endDate = (
            datetime.now()
            - timedelta(weeks=1)
            + timedelta(target_dayofweek - current_dayofweek)
        )
    return str(endDate).split()[0]
