import requests

__all__ = ["Parser"]


class Parser():
    def __init__(self):
        self.sess = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"
        }
        self.sess.headers.update(self.headers)
        self.timeout = 5
