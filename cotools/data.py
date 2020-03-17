import json
from os import listdir


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
        self.dir_dict = {idx: f for idx, f in enumerate(listdir(self.directory))}


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




