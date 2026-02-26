from user_agents import parse

def parse_user_agent(ua_string):
   
    if not ua_string:
        return {
            "browser": "Unknown",
            "os": "Unknown",
            "device": "Other"
        }
    
    ua = parse(ua_string)
    
    # Browser
    browser = ua.browser.family
    


    # OS
    os = ua.os.family
    

    
    # Device Classification
    if ua.is_mobile:
        device = "Mobile"
    elif ua.is_tablet:
        device = "Tablet"
    elif ua.is_pc:
        device = "Desktop"
    else:
        device = "Other"
        
    return {
        "browser": browser,
        "os": os,
        "device": device
    }
