from user_agents import parse

def is_bot_request(user_agent_string):
    if not user_agent_string:
        return False
        
    user_agent_string_lower = user_agent_string.lower()
    
    
    try:
        user_agent = parse(user_agent_string)
        if user_agent.is_bot:
            return True
    except Exception:
        pass
   
    bot_keywords = ['bot', 'spider', 'crawl', 'slurp', 'fetch', 'monitor']
    for keyword in bot_keywords:
        if keyword in user_agent_string_lower:
            return True
            
  
    headless_keywords = ['headlesschrome', 'phantomjs', 'selenium']
    for keyword in headless_keywords:
        if keyword in user_agent_string_lower:
            return True
            
    return False
