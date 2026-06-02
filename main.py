from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from routers import stations

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(stations.router)

stations_df = pd.read_csv("data_small/"
                          "stations.txt",
                        skiprows = 17)
stations_df = stations_df[["STAID",
                     "STANAME                                 "]]
stations_df.columns = ["STAID", "STANAME"]

all_stations = stations_df.to_dict(orient='records')
print(f"Всего станций в базе: {len(all_stations)}")

@app.get("/", response_class=HTMLResponse,
         response_model=None)
async def home(request: Request, page: int = 1):
    items_per_page = 50
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page

    stations_page = all_stations[start_idx:end_idx]

    total_pages = ((len(all_stations)
                   + items_per_page - 1)
                   // items_per_page)

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "stations": stations_page,
            "current_page": page,
            "total_pages": total_pages,
            "total_stations": len(all_stations),
            "has_prev": page > 1,
            "has_next": page < total_pages
        }
    )