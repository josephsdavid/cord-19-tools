import csv
from urllib.request import urlopen
import io

def _read_data(url: str) -> dict:
    response = urlopen(url)
    byts = response.read()
    data = io.StringIO(byts.decode())
    reader = csv.DictReader(data)
    result = {}
    for row in reader:
        for column, value in row.items():
            result.setdefault(column, []).append(value)
    return result

def _convert_data(data: dict) -> dict:
    out = {}
    for k in data.keys():
        if k in ['Province/State', 'Country/Region']:
            out[k] = data[k]
        elif k in ['Lat', 'Long']:
            out[k] = list(map(float, data[k]))
        else:
            out[k] = list(map(int, data[k]))
    return out

def get_hopkins() -> (dict, dict, dict):
    datafiles = ["https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv",
                 "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv",
                 "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"]
    return (_convert_data(_read_data(dat)) for dat in datafiles)
