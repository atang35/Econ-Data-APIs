# import libraries
import pandas as pd 
#import sqlalchemy
import numpy as np
#from sqlalchemy import create_engine
import datetime as dt 
import json
import matplotlib.pyplot as plt
import requests
import plotly.express as px
import datetime
from datetime import datetime 
import xmltojson



# class that will interate with FRED API 

# class that will interate with FRED API 

class FredPy:
    
    
    
    def __init__(self, token=None):
        self.token = token
        self.url = "https://api.stlouisfed.org/fred/series/observations" + \
                    "?series_id={seriesID}&api_key={key}&file_type=json" + \
                    "&observation_start={start}&observation_end={end}&units={units}"    
    
    
    
    def set_token(self, token):
        self.token = token
        
    
    
    
    
    def get_series(self, seriesID, start, end, units):
        
        """
    This function retrieves a time series data from the Federal Reserve Economic Data (FRED) API.
    
    Parameters:
    seriesID (str): The unique identifier for the series on FRED.
    start (str): The start date of the series in 'YYYY-MM-DD' format.
    end (str): The end date of the series in 'YYYY-MM-DD' format.
    units (str): The units of measurement for the series.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the date and value of the series. The date is in datetime format,
    and the value is converted to float. The column name of the value is the seriesID.
    
    Raises:
    Exception: If the API key is not provided or if the API returns a bad response.
    """

        url_formatted = self.url.format(
            seriesID=seriesID, 
            start=start, 
            end=end,  
            units=units,
            key=self.token # Replace with your API key or get the key from json secret file
            )
        
        response = requests.get(url_formatted)
        
        # if we get successful response, pull the data
        
        if(self.token):
            if (response.status_code == 200):
                data = pd.DataFrame(response.json()['observations'])[['date', 'value']]
                data = data.dropna(subset=['value'])
                data = data[pd.to_numeric(data['value'], errors='coerce').notnull()]\
                    .assign(date = lambda cols: pd.to_datetime(cols['date']))\
                    .assign(value = lambda cols: cols['value'].astype(float))\
                    .rename(columns = {'value' : seriesID})
                    
                
                return data    
            
            
            else:
                raise Exception("Bad response from API, status code = {}".format(response.status_code))
        else:
            raise Exception("No API key provided")   
        
        

# class that will interate with IMF API

if __name__ == "__main__":
    fred = FredPy()

