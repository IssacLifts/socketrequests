from .socketrequests_ import Socket
from .types_ import socketinfo
from .socketsession import SocketSession
from .errors import InvalidRequestType, InvalidCertificate, InvalidJson, InvalidRequest, InvalidURL
from typing import List
from ssl import SSLContext

def get(url: str,
        port: int, *,
        headers: List[str]=None,
        ssl: bool=False,
        bytes_amt: int=8192,
        ssl_certificate: SSLContext=None
        ) -> socketinfo:
    """Sends a 'GET' Request to the server
    Returns:
        socketinfo: response data
    """
    return Socket(url, port, ssl=ssl, bytes_amt=bytes_amt, ssl_certificate=ssl_certificate).send("GET", headers=headers)

def post(url: str,
         port: int, *,
         headers: List[str]=None,
         ssl: bool=False,
         json: List[str]=None,
         bytes_amt: int=8192,
         ssl_certificate: SSLContext=None
         ) -> socketinfo:
    """Sends a 'POST' Request to the server
    Returns:
        socketinfo: response data
    """
    return Socket(url, port, ssl=ssl, bytes_amt=bytes_amt, ssl_certificate=ssl_certificate).send("POST", headers=headers, json=json)

def put(url: str,
        port: int,
        *,
        headers: List[str]=None,
        ssl: bool=False,
        json: List[str]=None,
        bytes_amt: int=8192,
        ssl_certificate: SSLContext=None
        ) -> socketinfo:
    """Sends a 'PUT Request to the server
    Returns:
        socketinfo: response data
    """
    return Socket(url, port, ssl=ssl, bytes_amt=bytes_amt, ssl_certificate=ssl_certificate).send("PUT", headers=headers, json=json)

def delete(url: str,
           port: int,
           *,
           headers: List[str]=None,
           ssl: bool=False,
           json: dict=None,
           bytes_amt: int=8192,
           ssl_certificate: SSLContext=None
           ) -> socketinfo:
    """Sends a 'DELETE' Request to the server
    Returns:
        socketinfo: response data
    """
    return Socket(url, port, ssl=ssl, bytes_amt=bytes_amt, ssl_certificate=ssl_certificate).send("DELETE", headers=headers, json=json)

