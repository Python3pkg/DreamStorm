import queue
import random

from .Crawler import Crawler
from .lib.utils import daemonThread


class DreamStorm:
    def __init__(self, threads, tor=False):
        self.counter = 0
        self.threads = threads
        self.tor = tor
        self.q = (queue.Queue(), queue.Queue())
        self.qq = []
        for i in range(self.threads):
            self.qq.append((queue.Queue(), queue.Queue()))
            c = Crawler(self.qq[-1], self.tor)
            daemonThread(c.run)

    def idle(self):
        return self.counter == 0

    def put(self, url, headers={}, postdata={}):
        if type(url) != list:
            url = [url]
        for _url in url:
            self.counter += 1
            self.q[0].put({
                "url": _url,
                "headers": headers,
                "postdata": postdata
            })

    def run(self, callback):
        while self.counter:
            if not self.q[0].empty():
                rand = random.randint(0, self.threads - 1)
                self.qq[rand][0].put(self.q[0].get())
            for q in self.qq:
                if not q[1].empty():
                    package = q[1].get()
                    callback(package[0], package[1])
                    self.counter -= 1
