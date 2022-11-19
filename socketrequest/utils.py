from typing import List

DEFAULT_ACCEPT_ENCODING = "gzip, deflate"

def default_user_agent(name: str ='python-socketrequests') -> str:
    return f"{name}/0.01"

def default_headers() -> List[str]:
    return [
      f"User-Agent: {default_user_agent(name='python-socketrequests')}",
        f"Accept-Encoding: {DEFAULT_ACCEPT_ENCODING}",
        "Accept: */*",
        "Connection: keep-alive"
    ]
    
