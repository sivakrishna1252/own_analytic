import ipaddress
import geoip2.database
from django.conf import settings

def get_country_from_ip(ip_address_str):
    if not ip_address_str:
        return "Unknown"
        
    try:
        ip_obj = ipaddress.ip_address(ip_address_str)
        if ip_obj.is_loopback or ip_obj.is_private:
            return "Unknown"
            
        with geoip2.database.Reader(settings.GEOIP_DATABASE_PATH) as reader:
            response = reader.country(ip_address_str)
            return response.country.name or "Unknown"
            
    except Exception:
        return "Unknown"
