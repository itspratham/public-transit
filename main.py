import json
import re
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

class Item1(BaseModel):
    origin_station_id: str
    destination_station_id: str
    date: str

@app.get("/api/light-rail/")
async def root(item: Item):
    try:
        item = item.dict()
        try:
            datetime.strptime(item["date"],"%Y-%m-%d")
        except:
            return {"message": "Invalid Date Format."}
        datee = item["date"].split("-")
        year = datee[0]
        month = datee[1]
        date_ = datee[2]
        origin_station_id = item["origin_station_id"]
        destination_station_id = item["destination_station_id"]
        url = "https://traintime.lirr.org/api/TrainTime?month={}&day={}&year={}&datoggle=d&endsta={}&startsta={}&&api_key=dwrxfpcsp42pcwxfbpd90zde5fjeb05pcdaqjw3j".format(month, date_, year, destination_station_id, origin_station_id)
        x = requests.get(url)
        # print(x.json())
        item_list = x.json()
        a_list = []
        if len(item_list["TRIPS"]) == 0:
            return {"message": "0 trip found"}
        for i in range(len(item_list["TRIPS"])):
            dt = parser.parse(item["date"])
            start_ = datetime.strptime(item_list["TRIPS"][i]["LEGS"][0]["DEPART_TIME"], '%H%M').time()
            end_ = datetime.strptime(item_list["TRIPS"][i]["LEGS"][-1]["DEPART_TIME"], '%H%M').time()
            start_combined = datetime.strftime(dt.combine(dt, start_), "%m-%d-%Y %H:%M:%S")
            end_combined = datetime.strftime(dt.combine(dt, end_), "%m-%d-%Y %H:%M:%S")
            a_list.append({"eta_origin": start_combined, "eta_destination": end_combined})
        return {"transit mode": "light_rail", "time_slots": a_list}
    except:
        return {"message": "There is some error occurred while requesting"}

from dateutil import parser

@app.get("/api/rail/")
async def root1(item: Item):
    try:
        item = item.dict()
        try:
            datetime.strptime(item["date"],"%Y-%m-%d")
        except:
            return {"message": "Invalid Date Format."}
        datee = item["date"].split("-")
        year = datee[0]
        month = datee[1]
        date_ = datee[2]
        origin_station_id = item["origin_station_id"]
        destination_station_id = item["destination_station_id"]
        # url = "https://traintime.lirr.org/api/TrainTime?month={}&day={}&year={}&datoggle=d&endsta={}&startsta={}&&api_key=dwrxfpcsp42pcwxfbpd90zde5fjeb05pcdaqjw3j".format(month, date_, year, destination_station_id, origin_station_id)
        url = "https://mnorth.prod.acquia-sites.com/wse/MYmta/Trains/v4/{}/{}/DepartBy/{}/{}/{}/0000/9ea83a8a361efacd098b6c7f6a6e49c1/Tripstatus24".format(origin_station_id, destination_station_id, str(year), str(int(month)),
                                                                            str(int(date_)) )
        print(url)
        x = requests.get(url)
        # print(x.json())
        item_list = x.json()
        a_list = []
        if len(item_list["GetTripStatusJsonResult"]) == 0:
            return {"message": "0 trip found"}
        for i in range(len(item_list["GetTripStatusJsonResult"])):
            start_ = parser.isoparse(item_list["GetTripStatusJsonResult"][i]["OriginDateTime"])
            start_ = datetime.strftime(start_, "%m-%d-%Y %H:%M:%S")
            end_ = parser.isoparse(item_list["GetTripStatusJsonResult"][i]["DestinationDateTime"])
            end_ = datetime.strftime(end_, "%m-%d-%Y %H:%M:%S")
            a_list.append({"eta_origin": start_, "eta_destination": end_})
        return {"transit mode": "rail", "time_slots": a_list}
    except:
        return {"message": "There is some error occurred while requesting"}
