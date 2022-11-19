# socketrequests

http request libary made using sockets.

Higly experimental; not ready to use yet.

Developed by Issac (c) 2022

## Examples of how to use (Alpha Version)

Sending a request
```python
import socketrequest

status_code = socketrequest.get("www.google.com", port=80).status_code
```

Sending a request with headers
```python
import socketrequest

socketrequest.get("www.google.com", port=80, headers=["User-Agent: socketrequests", "Content-Length: 223"].headers)
```

Creating a session (Extremly buggy)
```python
from socketrequest.socketsession import SocketSession

# with context manager
with SocketSession() as session:
    session.get("www.google.com", port=80)

# without context manager
session = SocketSession()
session.get("www.google.com", port=80)
session.close()
```

Sending a request with json data
```python
import socketrequest

socketrequest.post("https://www.youtubelink/random", port=80, headers=["User-Agent Pandora"], json=["sdawd"])
```

### How to Install
```python
pip install socketrequest
```

