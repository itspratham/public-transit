import json
from datetime import datetime

from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
import requests
import dateutil.parser as parser
app = FastAPI()


class Item(BaseModel):
    origin_station_id: str
    destination_station_id: str
    date: str


@app.get("/")
async def root(item: Item):
    try:
        item = item.dict()
        datee = item["date"].split("-")
        print(datee)
        year = datee[0]
        month = datee[1]
        date_ = datee[2]
        origin_station_id = item["origin_station_id"]
        destination_station_id = item["destination_station_id"]
        url = "https://traintime.lirr.org/api/TrainTime?month={}&day={}&year={}&datoggle=d&endsta={}&startsta={}&&api_key=dwrxfpcsp42pcwxfbpd90zde5fjeb05pcdaqjw3j".format(month, date_, year, destination_station_id, origin_station_id)
        x = requests.get(url)
        item_list = x.json()
        a_list = []
        for i in range(len(item_list["TRIPS"])):
            dt = parser.parse(item["date"])
            start_ = datetime.strptime(item_list["TRIPS"][i]["LEGS"][0]["DEPART_TIME"], '%H%M').time()
            end_ = datetime.strptime(item_list["TRIPS"][i]["LEGS"][-1]["DEPART_TIME"], '%H%M').time()
            start_combined = datetime.strftime(dt.combine(dt, start_), "%m-%d-%Y %H:%M:%S")
            end_combined = datetime.strftime(dt.combine(dt, end_), "%m-%d-%Y %H:%M:%S")
            a_list.append({"eta_origin": start_combined, "eta_destination": end_combined})
        return [{"transit mode": "rail"}, a_list]
    except:
        return []
