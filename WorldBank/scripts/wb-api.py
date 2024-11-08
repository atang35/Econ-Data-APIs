# import necessary libraries
import pandas as pd
import numpy as np
import requests


# A class object that will be used to interact with World Bank API
class WBPy:

    def __init__(self):
        self.url = "https://api.worldbank.org/v2/" + \
                    "country/{country}/indicator/" + \
                    "{indicator}?/" + \
                    "&date={start}:{end}"

    def get_data(self, country, indicator, start, end):
        url = self.url.format(
            country=country, 
            indicator=indicator, 
            start=start, 
            end=end)
        
        response = requests.get(url)

        if (response.status_code == 200):
            
            print("Raw response text:", response.text)
            
            try:
                data = response.json()
            
                return data
            
            except ValueError:
                print("Error: Invalid JSON response")
                return None
        
        else:
            print(f"Error: {response.status_code}")
            return None


# initialize the class
wbpy = WBPy()

#lso_df = wbpy.get_data("LSO", "TT.PRI.MRCH.XD.WD", 1990, 2023)


chile_df = wbpy.get_data("CHL", "DP.DOD.DECD.CR.BC.CD",2013 , 2013)

# a function to interact with the World Bank API endpoint
#def get_wdb_data(country, indicator, start, end):
    #url = "http://api.worldbank.org/v2/country/" + \
        #"{country}/indicator/{indicator}?format=json&" + \
        #"per_page=500&date={start}:{end}"
    #response = requests.get(url)
    
    #if (response.status_code == 200):
        #data = pd.DataFrame(response.json())[['date']]
        #return data
        

#lesotho_df = get_wdb_data("LSO", "TT.PRI.MRCH.XD.WD", 1990, 2023)