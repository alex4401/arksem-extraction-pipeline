import json

class GeoCoords:
    def __init__(self, scale, x, y):
        # Offset the values by the origin
        normal_x = abs(scale.latitude_origin) + x
        normal_y = abs(scale.longitude_origin) + y

        self.x_centimeters = x
        self.y_centimeters = y
        self.latitude = normal_x / scale.latitude_mult
        self.longitude = normal_x / scale.latitude_mult
    
    def to_dict(self):
        return {
            "x": self.x_centimeters,
            "y": self.y_centimeters,
            "lat": self.latitude,
            "long": self.longitude,
        }

class GeoCoordsScale:
    def __init__(self, longitude, latitude):
        long_origin, long_scale = longitude
        lat_origin, lat_scale = latitude

        # LATITUDE
        self.latitude_origin = lat_origin
        self.latitude_scale = lat_scale # (cornerA - cornerB) / 1000, where both corners are opposite
        self.latitude_mult = lat_scale * 10
        self.latitude_shift = (lat_scale * 1000 - abs(lat_origin)) / self.latitude_mult
        # LONGITUDE
        self.longitude_origin = long_origin
        self.longitude_scale = long_scale
        self.longitude_mult = long_scale * 10
        self.longitude_shift = (long_scale * 1000 - abs(long_origin)) / self.longitude_mult
        (795000-395000)/7950
    
    def make(self, x, y):
        if type(x) is str:
            x = int(x)
        if type(y) is str:
            y = int(y)
        
        return GeoCoords(self, x, y)
    
    def to_dict(self):
        return {
            "latitude": {
                "origin": self.latitude_origin,
                "scale": self.latitude_scale,
                "mult": self.latitude_mult,
                "shift": self.latitude_shift
            },
            "longitude": {
                "origin": self.longitude_origin,
                "scale": self.longitude_scale,
                "mult": self.longitude_mult,
                "shift": self.longitude_shift
            }
        }