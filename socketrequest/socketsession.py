import socket
from ssl import SSLSocket
import ssl
from typing import List, Self
import json as _json
from urllib3.util.url import parse_url, Url

from socketrequest.types_ import socketinfo
from socketrequest.errors import InvalidRequestType, InvalidJson, InvalidCertificate, RequestError
from .socketrequests_ import Socket
from .utils import default_headers

class SocketSession(Socket):
    def __init__(self,
                 *,
                 ssl: bool =False,
                 bytes_amt: int=2048,
                 ssl_certificate=None,) -> None:
        """Socket based request libary, 100x faster than 'requests' libary

        Args:
            server (str): server url
            port (int): server port
            ssl (bool, optional): determines if the socket will be wrapped in SSL. Defaults to False.
            bytes_amt (int, optional): Bytes used to decode the data. Defaults to 8192.
        """
        self._ssl: bool = ssl
        self._bytes_amt: int = bytes_amt
        self._ssl_certificate = ssl_certificate
        self._sock: socket.socket | SSLSocket = None
        self._url = None
        
        self.default_headers = default_headers()
    
    def _build_socket(self, server: Url, port: int) -> socket.socket | SSLSocket:
        (sock := socket.socket(socket.AF_INET, socket.SOCK_STREAM)).connect((server.host, port))
        if self._ssl is None and self._ssl_certificate is None:
            return sock
        
        if self._ssl and self._ssl_certificate is not None:
            context = ssl.SSLContext(self._ssl_certificate)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.verify_mode = False
            return context.wrap_socket(sock, server_hostname=server.host)
        elif self._ssl and self._ssl_certificate is None:
            try:
                return ssl.create_default_context().wrap_socket(sock, server_hostname=server.host)
            except ssl.SSLCertVerificationError as e:
                if "Hostname mismatch, certificate is not valid for 'https'" in str(e):
                    raise
                
                else:
                    raise InvalidCertificate(
                        "Invalid SSL certificate type"
                    ) 
                
        
        return sock
    
    def _build_payload(self, server: Url, http_request: str, *, headers: List[str] = None, json: List[str] = None) -> str:
        payload: str = f"{http_request} {(server.path if server.path is not None else '/')}{(f'?{server.query}' if server.query is not None else '')} HTTP/1.1\r\nHost: {server.host}"

        
        for header in self.default_headers:
            if header.split(":")[0] not in headers if headers is not None else {}:
                payload += f"\r\n{header}"
            
        if headers is not None:
            for header in headers:
                payload += f"\r\n{header}"
                
        if json is not None:
            for data in headers:
                payload += f"\r\n{data}"
        
        payload += "\r\n\r\n"
        

        return payload
        
    def send(self, url: str, port: int, *, http_request_type: str, headers=None, json=None) -> socketinfo:
        server: Url = parse_url(url); self.url = url
        if self._sock is None:
            self._sock: socket.socket | SSLSocket = self._build_socket(server, port)
        else:
            pass
        if http_request_type not in ("GET", "POST", "DELETE", "PUT"):
            raise InvalidRequestType(
                f"{http_request_type} is not a valid/supported request type"
            )
        
        if http_request_type == "POST" and data is None:
            raise InvalidJson(
                "Json data is mandatory for 'POST' request method."
            )
            
        payload = self._build_payload(server=server,
                                      http_request=http_request_type,
                                      headers=headers if headers is not None and isinstance(headers, list) else None,
                                      json=json if json is not None and isinstance(json, list) else None
                                      )
        self._sock.send(bytes(payload, 'utf-8'))
        data = self._sock.recv(self._bytes_amt).decode('utf-8')
        return super()._parse_response(data, [*self.default_headers, *headers] if headers is not None else self.default_headers)
     
    
    def close(self) -> None:
        self.__exit__()
    
    def get(self, url: str, port: int, *, headers=None) -> socketinfo:
        return self.send(url, port, http_request_type="GET", headers=headers)
        
    def post(self, url: str, port: int, *, headers=None, data=None) -> socketinfo:
        return self.send(url, port, http_request_type="POST", headers=headers, json=data)

    def delete(self, url: str, port: int, *, headers=None, data=None) -> socketinfo:
        return self.send(url, port, http_request_type="DELETE", headers=headers, json=data)
        
    def put(self, url: str, port: int, *, headers=None, data=None) -> socketinfo:
        return self.send(url, port, http_request_type="PUT", headers=headers, json=data)
    
    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, *args, **kwargs) -> None:
        self._sock.close()
        
