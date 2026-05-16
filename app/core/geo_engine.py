from shapely.geometry import Polygon
from pyproj import Geod

def calculate_land_metrics(coordinates):
    """
    Takes a list of coordinate dictionaries and calculates the true geodesic 
    area and perimeter using the WGS84 ellipsoid.
    
    Expected input: [{'lat': 6.92, 'lng': 79.86}, ...]
    """
    if len(coordinates) < 3:
        return {"error": "A polygon must have at least 3 points."}

    # Extract Longitude (x) and Latitude (y) into a list of tuples
    # Note: Geo/Math systems usually read (Longitude, Latitude)
    lon_lat_list = [(pt['lng'], pt['lat']) for pt in coordinates]
    
    # Create a Shapely Polygon
    poly = Polygon(lon_lat_list)
    
    # Initialize the geodesic math engine (WGS84 is the GPS standard)
    geod = Geod(ellps="WGS84")
    
    # Calculate mathematically accurate area and perimeter
    area_sq_meters, perimeter_meters = geod.geometry_area_perimeter(poly)
    
    # geometry_area_perimeter can return negative area depending on the 
    # clockwise/counter-clockwise direction the user drew the polygon.
    # We use abs() to always return a positive area.
    area_sq_meters = abs(area_sq_meters)
    
    # Calculate useful conversions
    acres = area_sq_meters / 4046.856
    perches = area_sq_meters / 25.2929 # Common metric in South Asia
    
    return {
        "area_sqm": area_sq_meters,
        "perimeter_m": perimeter_meters,
        "acres": acres,
        "perches": perches,
        "status": "success"
    }