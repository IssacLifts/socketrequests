from requestsockets.socketsession import SocketSession
import msmcauth
from time import sleep
from requests import Session



with SocketSession() as session:
    print(session.get("www.google.com", port=80).status_code)
    print(session.get("www.google.com", port=80).status_code)
    print(session.get("www.google.com", port=80).status_code)
    print(session.get("www.google.com", port=80).status_code)

# session = socketrequests.SocketSession()
# print(session.get("www.google.com", port=80).status_code)
# sleep(5)
# print(session.get("www.google.com", port=80).status_code)
# session.close()

with Session() as session:
    print(session.get("http://www.google.com").status_code)
    print(session.get("http://www.google.com").status_code)
    print(session.headers)