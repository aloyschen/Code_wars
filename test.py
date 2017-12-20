import socket
import urllib.request
import urllib.error


class MyException(Exception):

    pass
try:
    urllib.request.urlopen("http://google.com", timeout = 2)
except urllib.error.URLError as e:
    print('time out')
    print(e.reason)
# urllib.request.urlopen("http://google.com", timeout = 1)