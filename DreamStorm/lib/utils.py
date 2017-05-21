import socks
import socket
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import threading


def daemonThread(target, args=()):
    t = threading.Thread(target=target, args=args)
    t.daemon = True
    t.start()


def tor_init():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket


def connect(url, headers, postdata):
    postdata = urllib.parse.urlencode(postdata)
    try:
        if postdata:
            request = urllib.request.Request(url, headers=headers, data=postdata)
        else:
            request = urllib.request.Request(url, headers=headers)
        opener = urllib.request.build_opener()
        response = opener.open(request)
    except:
        return "", {}
    page = response.read().decode("utf-8", "ignore")
    info = dict(response.info())
    return page, info
