import pygeohash as pgh

# Define the 4 corner points (replace these with your coordinates)
lat1, lon1 = 41.6, -81.6  # Top-left corner
lat2, lon2 = 41.6, -81.4  # Top-right corner
lat3, lon3 = 41.4, -81.6  # Bottom-left corner
lat4, lon4 = 41.4, -81.4  # Bottom-right corner

# Calculate bounding box
min_lat = min(lat1, lat2, lat3, lat4)
max_lat = max(lat1, lat2, lat3, lat4)
min_lon = min(lon1, lon2, lon3, lon4)
max_lon = max(lon1, lon2, lon3, lon4)

# Choose precision level (example using precision of 5)
precision = 5

# Approximate step distance for this precision level
lat_step = 0.01
lon_step = 0.01

# Generate geohashes within the bounding box
geohashes = set()
lat = min_lat
while lat <= max_lat:
    lon = min_lon
    while lon <= max_lon:
        geohash = pgh.encode(lat, lon, precision=precision)
        geohashes.add(geohash)
        lon += lon_step
    lat += lat_step

# Convert to list and print each geohash on a new line
geohashes = sorted(list(geohashes))
for geohash in geohashes:
    print(geohash)