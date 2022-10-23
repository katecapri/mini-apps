"""
Based on the information entered by the user, the location and magnitude of earthquakes are displayed.
Format for dates: YYYY-MM-DD
Format for other fields: float with '.'
"""

import requests

url = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
start_time = input('Enter the start time ')
end_time = input('Enter the end time ')
latitude = input('Enter the latitude ')
longitude = input('Enter the longitude ')
max_radius_km = input('Enter the max radius in km ')
min_magnitude = input('Enter the min magnitude ')
response = requests.get(url, headers={'Accept': 'application/json'}, params={
    'format': 'geojson',
    'starttime': start_time,
    'endtime': end_time,
    'latitude': latitude,
    'longitude': longitude,
    'maxradiuskm': max_radius_km,
    'minmagnitude': min_magnitude
})
data = response.json()
for num in range(len(data['features'])):
    print(f"{num + 1}. Place: {data['features'][num]['properties']['place']}. Magnitude:"
          f"{data['features'][num]['properties']['mag']}")
