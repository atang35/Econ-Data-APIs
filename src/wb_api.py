import requests
import pandas as pd
import json
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

class WBPy:
    def __init__(self):
        self.url = "https://api.worldbank.org/v2/" + \
                "country/{country}/indicator/{indicator}?" + \
                "format={format}&date={start}:{end}&per_page=100"

    def get_data(self, country, indicator, start, end, format):
        url = self.url.format(
            country=country,
            indicator=indicator,
            format=format,
            start=start,
            end=end
        )
        
        
        if format == "xml":

            response = requests.get(url)
            
            if response.status_code == 200:
                print("Data retrieved successfully!")
                
                try:
                    # Decode response content to handle BOM
                    response_text = response.content.decode("utf-8-sig")
                    root = ET.fromstring(response_text)
                    namespace = {"wb": "http://www.worldbank.org"}

                    # initialise the data object to append later
                    data = []
                    for item in root.findall("wb:data", namespace):
                        record = {
                            "Indicator": item.find("wb:indicator", namespace).text,
                            "Country": item.find("wb:country", namespace).text,
                            "CountryISO3": item.find("wb:countryiso3code", namespace).text,
                            "Date": item.find("wb:date", namespace).text,
                            "Value": item.find("wb:value", namespace).text
                        }
                        
                        # append each record to the data object
                        data.append(record)
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(data)
                    # Convert Value to numeric
                    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')  
                    
                    return df

                except ET.ParseError as e:
                    print(f"Error parsing XML: {e}")
                    return None
            else:
                print(f"Error: HTTP {response.status_code}")
                return None
            
            
        elif format == "json":
            
            response = requests.get(url)
            
            # what happens when we have successful response
            if response.status_code == 200:
                
                print("Data retrieved successfully!")
                
                try:
                    raw_data = response.json()
                    
                    records = raw_data[1]
                    
                    # initialise the data object to store our observation
                    data = [] 
                    
                    for record in records:
                        data.append(
                            {
                                "Indicator": record["indicator"]["value"],
                                "Country" : record["country"]["value"],
                                "CountryISO3" : record["countryiso3code"],
                                "Date" : record["date"],
                                "Value" : record["value"]
                            })
                        
                    df = pd.DataFrame(data)
                    return df

                except KeyError:
                    print("Error: Invalid response format")
                    return None
        else:
            print("Error: Unsupported format")
            return None


if __name__ == "__main__":
    wb = WBPy()
