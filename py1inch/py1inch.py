import json
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class APIClient:
    __API_URL = 'https://api.1inch.exchange/v2.0/'

    def __init__(self, api_url=__API_URL):
        self.api_url = api_url
        self.request_timeout = 60

        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
    
    def __request(self, url):
        try:
            response = self.session.get(url, timeout=self.request_timeout)
            response.raise_for_status()
            content = json.loads(response.content.decode('utf-8'))

            return content

        except Exception as e:
            try:
                content = json.loads(response.content.decode('utf-8'))
                raise ValueError(content)

            except json.decoder.JSONDecodeError:
                pass

            raise
    
    def isLife(self):
        request_url = f"{self.api_url}healthcheck"
        return self.__request(request_url)
    
    # Approve

    def getCallData(self):
        request_url = f"{self.api_url}approve/calldata"
        return self.__request(request_url)

    def getSpenderAddress(self):
        request_url = f"{self.api_url}approve/spender"
        return self.__request(request_url)

    # Quote/Swap

    def getQuote(self):
        request_url = f"{self.api_url}quote"
        return self.__request(request_url)

    def swap(self):
        request_url = f"{self.api_url}swap"
        return self.__request(request_url)

    # Protocols

    def getProtocols(self):
        request_url = f"{self.api_url}protocols"
        return self.__request(request_url)

    # Tokens

    def getTokens(self):
        request_url = f"{self.api_url}tokens"
        return self.__request(request_url)