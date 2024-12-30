from datetime import datetime
from zoneinfo import ZoneInfo
from astral import LocationInfo
from astral.sun import sun

# Define the location (e.g., New York, USA)
locationNY = LocationInfo("New York", "USA", "America/New_York", 40.7128, -74.0060)
locationCLE= LocationInfo("Glennan", "USA", "America/New_York", 41.5014414,-81.6097471)

# Get the current date in local time
local_timezoneNY = ZoneInfo(locationNY.timezone)
current_date = datetime.now(local_timezoneNY).date()

# Calculate the sun data for the location
s = sun(locationNY.observer, date=current_date)

# Extract the sunset time in UTC and convert to local timezone
sunset_utc = s["sunset"]
sunset_local = sunset_utc.astimezone(local_timezoneNY)

# Get the local date of sunset
sunset_date_local = sunset_local.date()

print(f"Sunset in {locationNY.name}: {sunset_local}")
print(f"Local date of sunset: {sunset_date_local}")

print('\n')
# Calculate the sun data for the location
local_timezoneCLE = ZoneInfo(locationCLE.timezone)
current_date = datetime.now(local_timezoneCLE).date()
s = sun(locationCLE.observer, date=current_date)

# Extract the sunset time in UTC and convert to local timezone
sunset_utc = s["sunset"]
sunset_local = sunset_utc.astimezone(local_timezoneCLE)

# Get the local date of sunset
sunset_date_local = sunset_local.date()

print(f"Sunset in {locationCLE.name}: {sunset_local}")
print(f"Local date of sunset: {sunset_date_local}")
