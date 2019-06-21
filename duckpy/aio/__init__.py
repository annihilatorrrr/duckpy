import random
import secrets
import certifi
import aiohttp
from .. import parse_page, ddg_url
from urllib.parse import unquote
from bs4 import BeautifulSoup


class Client:
    async def __init__(self, proxies=None, random_ua=True):
        if isinstance(proxies, type(None)):
            self.proxies = None
        elif isinstance(proxies, str):
            self.proxies = [proxies]
        elif isinstance(proxies, list):
            self.proxies = proxies

        self.http = await aiohttp.ClientSession()

        self.random_ua = random_ua

    async def search(self, query, **kwargs):
        if self.proxies:
            proxy = random.choice(self.proxies)
        if self.random_ua:
            headers = {'User-Agent': secrets.token_hex(5) + '/1.0'}
        else:
            headers = None

        r = await self.http.get(ddg_url, fields=dict(q=query, **kwargs), headers=headers)
        data = await r.read()

        return parse_page(data)
