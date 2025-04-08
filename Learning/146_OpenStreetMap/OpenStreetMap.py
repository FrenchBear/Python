# OpenStreetMap.py
# Show a map centered on a given location
# https://www.threads.net/@pythonclcoding/post/DEXyw9Tt3NO?xmt=AQGzU_jHclM9r_CLdxwz3gj8WQx4DCki59XMYjbzmtJ0cw
#
# 2025-01-10    PV

import webbrowser
import folium
from geopy.geocoders import Nominatim
from IPython.display import HTML  # noqa: F401“

location_name = input("Enter a location: ")

geolocator = Nominatim(user_agent="geoapi")
location = geolocator.geocode(location_name)

if location:
    # Create a map centered on the user's location
    latitude = location.latitude        # type: ignore
    longitude = location.longitude      # type: ignore
    clcoding = folium.Map(location=[latitude, longitude], zoom_start=12)

    marker = folium.Marker([latitude, longitude], popup=location_name)
    marker. add_to(clcoding)

    h = HTML(clcoding._repr_html_())
    htmlfile = r"c:\temp\my_file.html"
    with open(htmlfile, "w", encoding="utf-8") as f:
        f.write(str(h.data))
    webbrowser.open(htmlfile)
    #display(h)     # For Jupyter environments
else:
    print("Location not found. Please try again.")
