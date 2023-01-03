# public-transit

Step 1: git clone <reop-url>

Step 2: Create virtualenv and enable it to your project.

Step 3: pip install -r requirements.txt

Step 4: uvicorn main:app --reload

Step 5: Hit the postman with the url : http://127.0.0.1:8000/

Step 6: Pass these parameters in request body in the json_format

{
    "origin_station_id": "BSR",
    "destination_station_id": "BPG",
    "date": "2022-12-28"
}
Step 7:
{
    "origin_station_id": "85",
    "destination_station_id": "56",
    "date": "2023-01-04"
}
Step 7: You would get the result in output section.
