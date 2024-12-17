# import libraries

import pandas as pd 
import numpy as np
import datetime as dt 
from datetime import datetime
import json 
import requests
import xmltojson



# Create a class object
#https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH/USA/LSO/CHN/SWZ/ADVEC/periods=2019,2020

class IMFPy:
    
    def __init__(self):
        self.base_url = "https://www.imf.org/external/datamapper/api/v1/" + \
                        "{indicator}/{regions}/?periods={start_date},{end_date}" 
        
        
    def get_data(self, indicator, regions, start_date, end_date):
        url = self.base_url.format(
            indicator=indicator, 
            regions=regions, 
            start_date=start_date, 
            end_date=end_date
        )
        
        try:
        
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        
            if response.status_code == 200:
            
                data = []
            
                for region, values in response.json()['values'][indicator].items():
                    for date, value in values.items():
                        data.append(
                            {
                                'region': region, 
                                'date': int(date), 
                                'value': value
                            }
                        )
        
            return pd.DataFrame(data)
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data {e}")
            
            return None
        
        


imf = IMFPy()