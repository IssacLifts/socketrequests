import socket
from ssl import SSLSocket
import ssl
from typing import List
import json as _json
from urllib3.util.url import parse_url, Url

from requestsockets.utils import default_headers
from requestsockets.types_ import socketinfo
from requestsockets.errors import InvalidRequestType, InvalidJson, InvalidCertificate, RequestError

class Socket:
    def __init__(self,
                 server: str,
                 port: int,
                 *,
                 ssl: bool =False,
                 bytes_amt: int=8192,
                 ssl_certificate=None) -> None:
        """Socket based request libary, 100x faster than 'requests' libary

        Args:
            server (str): server url
            port (int): server port
            ssl (bool, optional): determines if the socket will be wrapped in SSL. Defaults to False.
            bytes_amt (int, optional): Bytes used to decode the data. Defaults to 8192.
        """
        self.url = server
        self._server: Url = parse_url(server)
        self._port: int = port
        self._ssl: bool = ssl
        self._bytes_amt: int = bytes_amt
        self._ssl_certificate = ssl_certificate
        self._sock: socket.socket | SSLSocket = self._build_socket()
        self.default_headers = default_headers() 
    
    def _build_socket(self) -> socket.socket | SSLSocket:
        (sock := socket.socket(socket.AF_INET, socket.SOCK_STREAM)).connect((self._server.host, self._port))
        if self._ssl is None and self._ssl_certificate is None:
            return sock
        
        if self._ssl and self._ssl_certificate is not None:
            context = ssl.SSLContext(self._ssl_certificate)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.verify_mode = False
            return context.wrap_socket(sock, server_hostname=self._server.host)
        elif self._ssl and self._ssl_certificate is None:
            try:
                return ssl.create_default_context().wrap_socket(sock, server_hostname=self._server.host)
            except ssl.SSLCertVerificationError as e:
                if "Hostname mismatch, certificate is not valid for 'https'" in str(e):
                    raise
                
                else:
                    raise InvalidCertificate(
                        "Invalid SSL certificate type"
                    ) 
                
        
        return sock
    
    def _build_payload(self, http_request: str, *, headers: List[str] = None, json: List[str] = None) -> str:
        payload: str = f"{http_request} {(self._server.path if self._server.path is not None else '/')}{(f'?{self._server.query}' if self._server.query is not None else '')} HTTP/1.1\r\nHost: {self._server.host}"
        
        for header in self.default_headers:
            if header.split(":")[0] not in headers if header is not None else {}:
                payload += f"\r\n{header}"
        
        if headers is not None:
            for header in headers:
                payload += f"\r\n{header}"
                
        if json is not None:
            for data in headers:
                payload += f"\r\n{data}"
        
        payload += "\r\n\r\n"
        
        return bytes(payload, "utf-8")
    
    
    def _parse_response(self, response: str, headers: List[str]) -> socketinfo:
        try:
            status = int(response[9:12])
        except ValueError:
            # don't know how to deal with this yet...
            status = None
    
        text = response
        
        try:
            json = _json.JSONDecoder().raw_decode(text.split("\r")[-1].replace("\n", ""))[0]
        except (IndexError, _json.JSONDecodeError):
            json = None
            
        if status == 200:
            ok = True
        else:
            ok = False
            
        url = self.url
        
        return socketinfo(
            status_code=status,
            url=url,
            ok=ok,
            json=json,
            headers=headers,
            text=text
        )
        
    def send(self, http_request_type: str, headers=None, data=None) -> socketinfo:
        if http_request_type not in ("GET", "POST", "DELETE", "PUT"):
            raise InvalidRequestType(
                f"{http_request_type} is not a valid/supported request type"
            )
        
        if http_request_type == "POST" and data is None:
            raise InvalidJson(
                "Json data is mandatory for 'POST' request method."
            )
            
        payload = self._build_payload(http_request=http_request_type,
                                      headers=headers if headers is not None and isinstance(headers, list) else None,
                                      json=data if data is not None and isinstance(data, list) else None
                                      )

        self._sock.send(payload)
        data = self._sock.recv(self._bytes_amt).decode("utf-8")
        return self._parse_response(data, [*self.default_headers, *headers] if headers is not None else self.default_headers)
