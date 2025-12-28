"""
class_Position.1.py
Finds lat/lon by GPS if that is available;
by WiFi if not.
Returns ditionary of lat: and lon:
v.1  Functions only.
TODO: Make into class.

"""

from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
import requests # http library https://pypi.org/project/requests/
import time

def get_gps_location(timeout=10):
    session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
    start = time.time()

    for report in session:
        if time.time() - start > timeout:
            break

        if report['class'] == 'TPV':
            lat = getattr(report, 'lat', None)
            lon = getattr(report, 'lon', None)
            if lat is not None and lon is not None:
                return {
                    "source": "gps",
                    "lat": lat,
                    "lon": lon
                }
    return None


def get_ip_location():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5)
        data = r.json()
        if "loc" in data:
            lat, lon = map(float, data["loc"].split(","))
            return {
                "source": "ip",
                "lat": lat,
                "lon": lon,
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country")
            }
    except Exception:
        pass
    return None

def get_location():
    diagnostic = False # set false for not printing in this function
    
    if diagnostic:
        gps_loc = get_gps_location()
        if gps_loc:
            print(gps_loc)
        ip_loc = get_ip_location()
        if ip_loc:
            print(ip_loc)
        return('')
            
    else:
        
        gps_loc = get_gps_location()
        if gps_loc:
            return gps_loc

        ip_loc = get_ip_location()
        if ip_loc:
            return ip_loc

        return {
            "source": "none",
            "error": "No location available"
        }
    
def extract_lat_lon(location):
    """
    Returns (lat, lon) tuple or None
    """
    if not isinstance(location, dict):
        return None

    try:
        return {
            "lat": float(location["lat"]),
            "lon": float(location["lon"]),
        }
        # return lat, lon as Python dictionary
    except (KeyError, TypeError, ValueError):
        return None


if __name__ == "__main__":
    loc = get_location()
    lat_lon = extract_lat_lon(loc)
    print(lat_lon)