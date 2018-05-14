# client interface
# CLI options
# proxy support
# splitting requests
# agent spoofing
# python 2 and 3 support

import os
from config import BASE_URL, AGENT

class Translator(object):
    def __init__(self, proxy=None, base_url=None, agent_spoof=AGENT,
                 session = None):
        self.proxies = proxy or os.getenv('HTTPS_PROXY')
        self.base_url = base_url or BASE_URL
        self.agent = agent_spoof

    @property
    def base_headers(self):
        pass

    def translate(self, text, from_lang='auto', to_lang='en'):
        pass

    def _raise_for_status(self):
        pass

    def _split_request(text):
        pass

    def _make_request(text, from_lang, to_lang):
        pass