import googlemaps
import json
import numpy as np
import pandas as pd
import requests

#ACO states
headers = {
    'accept': 'application/json',
}

params = {
    'offset': '0',
    'size': '5000',
}

response = requests.get(
    'https://data.cms.gov/data-api/v1/dataset/9767cb68-8ea9-4f0b-8179-9431abc89f11/data',
    params=params,
    headers=headers,
)
y = json.dumps(response.json())
data=pd.read_json(y)

params = {
    'offset': '5000',
    'size': '10000',
}

response = requests.get(
    'https://data.cms.gov/data-api/v1/dataset/9767cb68-8ea9-4f0b-8179-9431abc89f11/data',
    params=params,
    headers=headers,
)
y = json.dumps(response.json())
data1=pd.read_json(y)


params = {
    'offset': '10000',
    'size': '15000',
}

response = requests.get(
    'https://data.cms.gov/data-api/v1/dataset/9767cb68-8ea9-4f0b-8179-9431abc89f11/data',
    params=params,
    headers=headers,
)
y = json.dumps(response.json())
data2=pd.read_json(y)


params = {
    'offset': '15000',
    'size': '20000',
}

response = requests.get(
    'https://data.cms.gov/data-api/v1/dataset/9767cb68-8ea9-4f0b-8179-9431abc89f11/data',
    params=params,
    headers=headers,
)
y = json.dumps(response.json())
data3=pd.read_json(y)
frames = [ data, data1,data2,data3] #df19 is creating problem
dataz = pd.concat(frames,axis=0)
dataz=dataz.drop_duplicates(subset=['aco_id',"aco_service_area"])
dataz=dataz.reset_index()
dataz=dataz.rename(columns={"aco_id":"ACO_ID","aco_service_area":"ACO_State"})


dataz["lat"]=np.nan
dataz["long"]=np.nan
gmaps = googlemaps.Client(key='xxx')

for x in range(len(dataz)):
    address=dataz.iloc[x]["aco_address"]
    geocode_result = gmaps.geocode(address)
    try:
        lat=geocode_result[0].get("geometry").get("bounds").get("northeast").get('lat')
        dataz.at[x,"lat"]=lat
    except:
        lat=geocode_result[0].get("geometry").get("location").get('lat')
        dataz.at[x,"lat"]=lat
    try:
        dataz.at[x,"long"]=geocode_result[0].get("geometry").get("bounds").get("northeast").get('lng')
    except:
        dataz.at[x,"long"]=geocode_result[0].get("geometry").get("location").get('lng')

dataz.to_csv("aco_addresses_geocoded.csv")
        
"""
# Alternate approach without  googlemaps package
# 
secret="xxx"

for x in range(len(dataz)):
    address=dataz.iloc[x]["aco_address"]
    response = requests.get(
    f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={secret}",
    )  
    print(response.json())
    try:
        lat=response.json().get("results")[0].get("geometry").get("bounds").get("northeast").get('lat')
        dataz.at[x,"lat"]=lat
    except:
        lat=response.json().get("results")[0].get("geometry").get("location").get('lat')
        dataz.at[x,"lat"]=lat
    try:
        dataz.at[x,"long"]=response.json().get("results")[0].get("geometry").get("bounds").get("northeast").get('lng')
    except:
        dataz.at[x,"long"]=response.json().get("results")[0].get("geometry").get("location").get('lng')
"""