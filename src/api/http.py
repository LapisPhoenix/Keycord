import aiohttp
import src
from typing import Optional, Dict


# Constants

FULL_URL = (
    src.API_BACKEND
    if not src.API_BACKEND.endswith('/') else src.API_BACKEND[:-1]
)

HEADERS = {
    "Authorization": src.TOKEN,
    "User-Agent": src.USER_AGENT
}

API_BACKEND = (
    "%(url)s/%(version)s" % {"version": src.VERSION, "url": FULL_URL}
)


class AHttpClient:
    """
    Send Asynchronous requests
    """

    @staticmethod
    async def get(endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Get data from an endpoint
        :param endpoint: Request Endpoint
        :param params: Optional parameters
        :return:
        """

        async with aiohttp.ClientSession() as s:
            async with s.get(
                url=API_BACKEND + endpoint,
                headers=HEADERS,
                params=params
            ) as r:
                return await r.json()

    @staticmethod
    async def post(endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """
        Post data to an endpoint
        :param endpoint: Request Endpoint
        :param data: Optional Post Data
        :param params: Optional parameters
        :return:
        """

        async with aiohttp.ClientSession() as s:
            async with s.post(url=API_BACKEND + endpoint, headers=HEADERS, params=params, data=data) as r:
                return await r.json()
