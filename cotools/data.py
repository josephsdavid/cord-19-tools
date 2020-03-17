import json
from os import listdir


class Paperset:
    def __init__(self, directory: str) -> None:
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




