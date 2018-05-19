# client interface
# CLI options
# proxy support
# splitting requests
# agent spoofing
# python 2 and 3 support
# use html.unescape rather than html.parser

import os
from requests import Session
from urllib.parse import urlencode, quote_plus

from config import BASE_URL, AGENT

BASE_URL = "http://translate.google.com/"

class Translator(object):
    def __init__(self, proxies=None, base_url=BASE_URL, agent_spoof=AGENT,
                 session = None, split_requests=True):
        """
        Args:
            proxies (None, optional): Description
            base_url (TYPE, optional): Description
            agent_spoof (TYPE, optional): Description
            session (None, optional): Description
            split_requests (bool, optional): Description
        """
        self.proxies = proxies or os.getenv('HTTPS_PROXY')
        self.base_url = base_url.rstrip('/')
        self.agent = agent_spoof
        self.session = session or Session()
        self.split_requests = split_requests
    
    def translate(self, text, from_lang='auto', to_lang='en'):
        """Main method
        
        Args:
            text (TYPE): Description
            from_lang (str, optional): Description
            to_lang (str, optional): Description
        """
        if (len(text) > 5000) and self.split_requests:
            text_segments = _split_request(text)
        else:
            text_segments = [text]

        for t in text_segments:
            url = self._construct_url(t, from_lang, to_lang)

            resp = self._make_request(url)

            # parse resp content here and stuff

    def _construct_url(self, text, from_lang, to_lang):
        """
        Args:
            text (TYPE): Description
            from_lang (TYPE): Description
            to_lang (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        params = {'hl' : to_lang,
                  'sl' : from_lang,
                  'q': text}
        encoded_url =  self.base_url + '/m?' + urlencode(f)
        return encoded_url

    def _parse_content(self, resp):
        """Gets translation from response
        
        Args:
            resp (TYPE): Description
        """
        expr = r'class="t0">(.*?)<'
        re_result = re.findall(expr, resp.content)
        if (len(re_result) == 0):
            result = ""
        else:
        result = self.unescape(re_result[0])
        return (result)

    def unescape(self, text):
        if (sys.version_info[0] < 3):
            parser = HTMLParser.HTMLParser()
        else:
            parser = html.parser.HTMLParser()
        return (parser.unescape(text))


    def _split_request(text):
        """splits large requests into multiple
        
        Args:
            text (TYPE): Description
        """

    def _make_request(self, url):
        """
        Args:
            url (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        with closing(self.session.get(url=url,
                                      headers=agent,
                                      proxies=self.proxies
                                      )
                     ) as resp:
            resp.raise_for_status()
            return resp



if __name__ == '__main__':
    #do CLI stuff here






def _construct_url(text='hello friend', from_lang='en', to_lang='fr'):
    """
    """
    f = { 'hl' : to_lang, 'sl' : from_lang, 'q': text}
    return BASE_URL + '/m?' + urlencode(f)













