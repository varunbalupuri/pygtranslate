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

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser


from config import BASE_URL, AGENT

BASE_URL = "http://translate.google.com/"


class Translator(object):

    def __init__(self, proxies=None, base_url=BASE_URL, agent_spoof=AGENT,
                 session=None, split_requests=True, request_limit=5000):
        """
        Args:
            proxies (None, optional): http/https proxies
            base_url (str, optional): base API url
            agent_spoof (dict, optional): Fake agent details for request
            session (None, optional): Pass an existing requests.Session
            split_requests (bool, optional): Flag to enable request
                splitting functionality
            request_limit (int, optional): charachter limit for requests
        """
        self.proxies = proxies or os.getenv('HTTPS_PROXY')
        self.base_url = base_url.rstrip('/')
        self.agent = agent_spoof
        self.session = session or Session()
        if split_requests and (request_limit > 0):
            self.split_requests = split_requests
            self.request_limit = request_limit
        else:
            raise ArgumentError('request limit must be > 0 \
                                 if split_requests is used')

    def translate(self, text, from_lang='auto', to_lang='en'):
        """Main method for translation via Google Translate API

        Args:
            text (str): text to translate
            from_lang (str, optional): language of text, if not specified
                language detection will be used.
            to_lang (str, optional): language to translate to. If not
                specified, will default to english
        Returns:
            (str) : translated text body
        """
        if (len(text) > self.request_limit) and self.split_requests:
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
        params = {'hl': to_lang,
                  'sl': from_lang,
                  'q': text}
        encoded_url = self.base_url + '/m?' + urlencode(f)
        return encoded_url

    def _parse_content(self, resp):
        """Gets translation from response

        Args:
            resp (TYPE): Description

        Returns:
            TYPE: Description
        """
        expr = r'class="t0">(.*?)<'
        re_result = re.findall(expr, resp.content)
        if (len(re_result) == 0):
            result = ""
        else:
            parser = HTMLParser()
            parser.unescape(re_result[0])
        return (result)

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

    def splitter(text, max_chunk_size):
        """ Splits text into list of strings,
        guarenteeing that no chunk ever
        exceeds max_chunk_size in length AND the text is split
        on end of sentence markers preferebly or whitespace where
        physically possible with the above constraint

        Args:
            text (str): text string to split
            max_chunk_size (int): the maximum allowed size of any substring

        Returns:
            (list[str]): list of substrings
        """

        # if input is already short enough, just need one chunk
        rem_length = len(text)
        if rem_length < max_chunk_size:
            return [text]

        chunks = []
        prev_cut_off = 0
        chunk = None

        while chunk != '':
            cut_off = prev_cut_off + _cutoff_point(
                                            text[prev_cut_off:
                                                 prev_cut_off + max_chunk_size
                                                 ]
                                            )
            chunk = text[prev_cut_off: cut_off]

            rem_length -= len(chunk)
            chunks.append(chunk)

            prev_cut_off = cut_off
            # when remaining length is less than max allowed, exit.
            if rem_length < max_chunk_size:
                break

        # now append the last chunk.
        final_chunk = text[cut_off:]
        chunks.append(final_chunk)

        return chunks

    def _cutoff_point(text, stops=' .,?!:'):
        """Iterates through a string backwards
        until the first suitable end of sentence marker
        or whitespace is encountered where possible.

        Args:
            text (str): text to cut at designated points as defin

        Returns:
            (int): the index in the text of the optimal split point
            if this exists, else, simply the full string.
        """

        length = len(text)

        i = 1
        while True:
            if text[-i] in stops:
                return length - i

            if i == length-1:
                return length

            i += 1



if __name__ == '__main__':
    #do CLI stuff here






    def _construct_url(text='hello friend', from_lang='en', to_lang='fr'):
        """
        """
        f = { 'hl' : to_lang, 'sl' : from_lang, 'q': text}
        return BASE_URL + '/m?' + urlencode(f)













