"""
class_Position.2.py
Finds lat/lon by GPS if that is available;
by WiFi if not.
Returns ditionary of lat: and lon:
v.1  Functions only.
TODO: Make into class.
v.2  Start making into a class
  State variables:
    dictionary pos that contains lat and lon
  
  Methods:
    get_fix() that sets lat and lon
    
17 December 2025
Reads GPS or WiFi, produces dictionary with lat/lon.

"""
from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
import requests # http library https://pypi.org/project/requests/
import time

class Position:
    def __init__(self):
        self.pos = {'lat': 41.5, 'lon': -81.6} # Cleveland default
        self.get_fix()
        

    def get_gps_location(self, timeout=10):
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


    def get_ip_location(self):
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

    def get_location(self):
        diagnostic = False # set false for not printing in this function
        
        if diagnostic:
            gps_loc = self.get_gps_location()
            if gps_loc:
                print(gps_loc)
            ip_loc = self.get_ip_location()
            if ip_loc:
                print(ip_loc)
            return('')
                
        else:
            
            gps_loc = self.get_gps_location()
            if gps_loc:
                return gps_loc

            ip_loc = self.get_ip_location()
            if ip_loc:
                return ip_loc

            return {
                "source": "none",
                "error": "No location available"
            }
        
    def extract_lat_lon(self, location):
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
        
    def get_fix(self):
        loc = self.get_location()
        self.pos = self.extract_lat_lon(loc)


if __name__ == "__main__":
    Pos = Position()  # instantiate an object
    print(Pos.pos)    # object state variable is dictionary with lat and lon