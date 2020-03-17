import json
import os
from urllib.request import urlopen
import tarfile


class Paperset:
    def __init__(self, directory: str) -> None:
        """
        The Paperset class:
            __init__ args:
                directory: a string, the directory where the jsons are stored

            description:
                lazy loader for cord-19 text files. Data is not actually loaded
                until indexing, until then it just indexes files. Can be
                indexed with both ints and slices.
        """
        self.directory = directory
        self.dir_dict = {idx: f for idx, f in enumerate(os.listdir(self.directory))}


    def _load_file(self, path: str) -> dict:
        with open(f"{self.directory}/{path}") as handle:
            outdict = json.loads(handle.read())
        return outdict


    def __getitem__(self, indices: int) -> list:
        slicedkeys = list(self.dir_dict.keys())[indices]
        if not isinstance(slicedkeys, list):
            slicedkeys=[slicedkeys]
        return [self._load_file(self.dir_dict[key]) for key in slicedkeys]


    def __len__(self) -> int:
        return len(self.dir_dict.keys())




def download(dir: str='.') -> None:
    data = {
        'comm_use_subset':"https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/comm_use_subset.tar.gz",
        'noncomm_use_subset':"https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/noncomm_use_subset.tar.gz",
        'pmc_custom_license':"https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/pmc_custom_license.tar.gz",
        'biorxiv_medrxiv':"https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/biorxiv_medrxiv.tar.gz"
    }
    if not os.path.exists(dir):
        os.mkdir(dir)
    for d in data.keys():
        handle = urlopen(data[d])
        with open(f"{dir}/{d}.tar.gz", 'wb') as out:
            while True:
                dat = handle.read(1024)
                if len(dat) == 0: break
                out.write(dat)
    for f in os.listdir(dir):
        if tarfile.is_tarfile(f"{dir}/{f}"):
            tar = tarfile.open(f"{dir}/{f}", 'r:gz')
            tar.extractall(path=dir)
            tar.close()
            os.remove(f"{dir}/{f}")



