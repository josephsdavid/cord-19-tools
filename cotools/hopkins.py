import csv
import io
from typing import Any, Dict, Tuple
from urllib.request import urlopen


def _read_data(url: str) -> Dict[Any, Any]:
    response = urlopen(url)
    byts = response.read()
    data = io.StringIO(byts.decode())
    reader = csv.DictReader(data)
    result = {}
    for row in reader:
        for column, value in row.items():
            result.setdefault(column, []).append(value)
    return result


def _convert_data(data: Dict[Any, Any]) -> Dict[Any, Any]:
    out = {}
    for k in data.keys():
        if k in ["Province/State", "Country/Region"]:
            out[k] = data[k]
        elif k in ["Lat", "Long"]:
            out[k] = list(map(float, data[k]))
        else:
            out[k] = list(map(int, data[k]))
    return out


def get_hopkins() -> Tuple[Dict[Any, Any], Dict[Any, Any]]:
    datafiles = [
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
    ]
    print("Warning: Hopkins data is constantly changing!")
    return (_convert_data(_read_data(dat)) for dat in datafiles)


# url="https://docs.google.com/spreadsheets/d/1ZGol4qZthAc7wiElRYG_36iYT2own_W0QOiD3epGByY/export?gid=0&format=csv"
#
# url = "https://docs.google.com/spreadsheet/ccc?key=1ZGol4qZthAc7wiElRYG_36iYT2own_W0QOiD3epGByY&output=csv"
#
# url="https://drive.google.com/file/d/10Kffl2xAfWxiR_qtkgBSFu1gLuogmBad/export?gid=0&format=csv"
#
# import requests
# io.StringIO(requests.get(url).content)
#
# test = _read_data(url)
#
# test
#
# url2 = "docs.google.com/feeds/download/spreadsheets/Export?key<1ZGol4qZthAc7wiElRYG_36iYT2own_W0QOiD3epGByY>&exportFormat=csv&gid=0"
#
# _read_data(url2)
#
# test
#
# test.keys()
