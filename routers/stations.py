from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
import pandas as pd

router = APIRouter(
    prefix="/stations",
    tags=["Станции"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/{station}")
def about(station: str):
    filename = ("data_small/TG_STAID"
                + str(station).zfill(6) + ".txt")
    df = pd.read_csv(filename, skiprows=20,
                     parse_dates=["    DATE"])
    result = df.to_dict(orient='records')
    return result

@router.get("/{station}/{date}")
def all_data(station: str, date: str):
    filename = ("data_small/TG_STAID"
                + str(station).zfill(6) + ".txt")
    df = pd.read_csv(filename, skiprows=20,
                     parse_dates=["    DATE"])
    temperature = (df.loc[df['    DATE']
                == date]['   TG'].squeeze() / 10)
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


@router.get("/{station}/{year}")
def yearly(station: str, year: str):
    filename = ('data_small/TG_STAID' +
                str(station).zfill(6) + '.txt')
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))]
    result = result.to_dict(orient='records')
    return result


