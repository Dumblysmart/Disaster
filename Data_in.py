import requests
import xml.etree.ElementTree as ET
import json
import time

# GDACS API endpoint for recent disasters
url = "https://www.gdacs.org/xml/rss.xml"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

max_retries = 3
for attempt in range(max_retries):
    try:
        response = requests.get(url, headers=headers, timeout=30)  # Increased timeout
        response.raise_for_status()
        break
    except requests.exceptions.Timeout:
        print(f"Timeout occurred, retrying ({attempt + 1}/{max_retries})...")
        time.sleep(2)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        exit(1)
else:
    print("Failed to fetch data after multiple attempts.")
    exit(1)

root = ET.fromstring(response.content)

# Namespace for parsing
ns = {
    'gdacs': 'http://www.gdacs.org',
    'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#'
}

disasters = []
print(f"Found {len(root.findall('.//item'))} items in the feed.")
for item in root.findall('.//item'):
    title_elem = item.find('title')
    title = title_elem.text if title_elem is not None else None
    lat_elem = item.find('geo:lat', ns)
    lon_elem = item.find('geo:long', ns)
    print(f"title: {title}, lat_elem: {lat_elem}, lon_elem: {lon_elem}")  # Debug print
    if title and lat_elem is not None and lon_elem is not None:
        lat = lat_elem.text
        lon = lon_elem.text
        disasters.append({'title': title, 'lat': lat, 'lon': lon})

