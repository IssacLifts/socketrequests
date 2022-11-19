from typing import NamedTuple as namedtuple

class socketinfo(namedtuple):
    status_code: int
    url: str
    ok: bool
    json: dict
    headers: dict
    text: str
    
