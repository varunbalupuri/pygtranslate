# -*- coding: utf-8 -*-
import os
from re import findall
import logging
from requests import Session
from contextlib import closing

try:
    from html.parser import HTMLParser
    from urllib.parse import urlencode, quote_plus
except ImportError:
    # handle python 2.
    from HTMLParser import HTMLParser
    from urllib import urlencode, quote_plus

BASE_URL = "http://translate.google.com/"

AGENT = {'User-Agent':
         "Mozilla/4.0 (\
          compatible;\
          MSIE 6.0;\
          Windows NT 5.1;\
          SV1;\
          .NET CLR 1.1.4322;\
          .NET CLR 2.0.50727;\
          .NET CLR 3.0.04506.30\
          )"
         }


class Translator(object):
    """ Pythonic interface to Google Translate API for Python 2.7 and 3.x
    with command line interface and proxy support.
    Supports splitting or large requests to allow large queries.
    """
    def __init__(self, proxy=None, base_url=BASE_URL, agent_spoof=AGENT,
                 session=None, split_requests=True, logger=None):
        """
        Args:
            proxies (None, optional): http/https proxies
            base_url (str, optional): base API url
            agent_spoof (dict, optional): Fake agent details for request
            session (None, optional): Pass an existing requests.Session
            split_requests (bool, optional): Flag to enable request
                splitting functionality
            logger (python logger): default logger
        """
        proxy = proxy or os.getenv('HTTPS_PROXY')
        if proxy is not None:
            self.proxies = {'HTTPS_PROXY': proxy}
        else:
            self.proxies = None
        self.base_url = base_url.rstrip('/')
        self.agent = agent_spoof
        self.session = session or Session()
        self.split_requests = split_requests
        self.logger = logger or logging.getLogger(__name__)

    def translate(self, text, from_lang='auto', to_lang='en',
                  max_chunk_size=4000):
        """Main method for translation via Google's free Translate API
        
        Usage:
        ________________________________________________

        client = Translator()
        client.translate('Bonjour', from_lang='fr')
        ________________________________________________
    
        Args:
            text (str): text to translate
            from_lang (str, optional): language of text, if not specified
                language detection will be used.
            to_lang (str, optional): language to translate to. If not
                specified, will default to english
            max_chunk_size (int, optional): charachter limit for requests
        Returns:
            (str) : translated text body
        """
        if (len(text) > max_chunk_size) and (self.split_requests):
            text_segments = self._split_request(text, max_chunk_size)
            self.logger.info('chunked text segments are: {}'.format(text_segments))
        else:
            text_segments = [text]
            self.logger.info('using single text segment')

        output = []
        for t in text_segments:
            url = self._construct_url(t, from_lang, to_lang)
            resp = self._make_request(url)
            body = self._parse_content(resp)
            output.append(body)

        return ''.join(output).replace(u'\xa0', u' ')

    def _construct_url(self, text, from_lang, to_lang):
        """Encodes url in required format.

        Args:
            text (str): query text
            from_lang (str): language to translate FROM
            to_lang (str): language to translate TO

        Returns:
            (str): encoded url
        """
        params = {'hl': to_lang,
                  'sl': from_lang,
                  'q': text}
        encoded_url = self.base_url + '/m?' + urlencode(params)
        self.logger.info('query URI: {}'.format(encoded_url))
        return encoded_url

    def _parse_content(self, resp):
        """Gets translation text body from response

        Args:
            resp (requests.Response): Repsonse object from
                API call

        Returns:
            str: translated text from the html block
        """
        expr = r'class="t0">(.*?)<'
        re_result = findall(expr, resp.text)
        if (len(re_result) == 0):
            result = ""
            self.logger.warning('found no valid translated text body')
        else:
            parser = HTMLParser()
            result = parser.unescape(re_result[0])
        return result

    def _make_request(self, url):
        """
        Args:
            url (str): valid API URI

        Returns:
            (requests.Response): response of request
        """
        self.logger.debug('making request to url')
        with closing(self.session.get(url=url,
                                      headers=self.agent,
                                      proxies=self.proxies
                                      )
                     ) as resp:
            resp.raise_for_status()
            self.logger.debug('resp: {}'.format(resp))
            return resp

    def _split_request(self, text, max_chunk_size):
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

        rem_length = len(text)

        chunks = []
        prev_cut_off = 0
        chunk = None

        while chunk != '':
            cut_off = prev_cut_off + self._cutoff_point(
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

    def _cutoff_point(self, text, stops=' .,?!:'):
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
    
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Google Translate API.')
    
    parser.add_argument('-t', '--to',
                         dest='to_lang', action='store',
                         default = 'en'
                         )
    parser.add_argument('-f', '-from',
                         dest ='from_lang', action='store',
                         default = 'auto'
                         )
    parser.add_argument('-q', '-query',
                        dest = 'query',action='store',
                        default = None
                        )
    args = parser.parse_args()
    
    if args.query is None:
        sys.exit('Query text must be non-empty')

    # translate
    client = Translator()
    text = client.translate(to_lang=args.to_lang,
                     from_lang=args.from_lang,
                     text = args.query
                     )

    print(text)


