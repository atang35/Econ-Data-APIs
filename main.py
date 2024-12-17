from src.wb_api import WBPy
from src.fred_api import FredPy
from src.imf_api import IMFPy
import json
import datetime as dt

# World Bank API

wb = WBPy()

wb_data = wb.get_data(
    country="USA",
    indicator="SP.POP.TOTL",
    start="1960",
    end="2020",
    format="json"
)


print(wb_data.head())


# FRED series 

fred = FredPy()


# api key

with open('FRED/secrets.json', 'r') as file:
    secrets = json.load(file)

api_key = secrets['api_key'] 


# now parse the api key 

fred.set_token(api_key)  

fred_data =fred.get_series(
    seriesID = 'DGS10', # 10 year Treasury yield
    start = '2000-01-01', #
    end = dt.datetime.now().strftime('%Y-%m-%d'),
    units = 'lin'
)

print(fred_data.head())


# IMF API 

imf = IMFPy()

imf_data = imf.get_data(
    indicator="NGDP_RPCH",
    regions="USA/LSO",
    start_date=1980,
    end_date=2022
)

print(imf_data.head())
