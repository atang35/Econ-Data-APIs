import requests
import xml.etree.ElementTree as ET

# A class object that will be used to interact with the World Bank API
class WBPy:

    def __init__(self):
        self.url = "https://api.worldbank.org/v2/" + \
                    "country/{country}/indicator/" + \
                    "{indicator}?" + \
                    "date={start}:{end}&format=json"

    def get_data(self, country, indicator, start, end):
        url = self.url.format(
            country=country, 
            indicator=indicator, 
            start=start, 
            end=end
        )
        
        response = requests.get(url)

        if response.status_code == 200:
            print("Raw response text:", response.text)
            try:
                # Parse the XML response
                root = ET.fromstring(response.content)
                
                # Extract data - customize based on XML structure
                data = []
                for data_point in root.findall(".//data"):
                    date = data_point.find("date").text
                    value = data_point.find("value").text if data_point.find("value") is not None else None
                    data.append({"date": date, "value": value})
                
                return data
            
            except ET.ParseError:
                print("Error: Unable to parse XML response")
                return None
        
        else:
            print(f"Error: {response.status_code}")
            return None


# Initialize the class and make a call to get data
wbpy = WBPy()