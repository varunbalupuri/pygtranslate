# -*- coding: utf-8 -*-

import pytest
import mock
from six import string_types

from gtranslate import Translator

class MockResp(object):
    def __init__(self, code=200, text=None):
        self.status_code = code
        self.text = text

    def close(self):
        pass

    def raise_for_status(self):
        if self.status_code > 400:
            raise Exception


class MockSession(object):
    def __init__(self, code=200, text=None):
        self.code = code
        self.text = text
    
    def get(self, **kwargs):
        return MockResp(code = self.code, text=self.text)

    def close(self):
        pass    

raw_html = '''<html><head><title>Google Traduction</title><style>body{font:normal small arial,sans-serif,helvetica}body,html,form,div,p,img,input{margin:0padding:0}body{padding:3px}.nb{border:0}.s1{padding:5px}.ub{border-top:1px solid #36c}.db{border-bottom:1px solid #36c}.blue{background:#ebeff9}.pt{padding-top:5px}form{padding:5px 5px 3px}.s2{padding-top:2px;padding-bottom:2px}div{border:1px solid #fff}html,body{background:#fff}body{padding-top:6px}.small{font-size:small}.title{vertical-align:middle}.center{text-align:center}#arrow{padding:5px;vertical-align:-1px;text-decoration:none}.t0{font-size:large;padding-bottom:2px}.o1{color:gray}</style><meta content="text/html; charset=UTF-8" http-equiv="content-type"/></head><body dir="ltr"><div><img class="title" height="16" width="48" src="https://www.gstatic.com/images/branding/googlelogo/1x/googlelogo_color_48x16dp.png"alt="Google" style="margin-top: -2px"/>&nbsp;<span class="small">Traduction</span></div><form action="/m?hl=fr&amp;sl=en&amp;q=hello"><input type="hidden" name="hl" value="fr"/><input type="hidden" name="sl" value="en"/><input type="hidden" name="tl" value="fr"/><input type="hidden" name="ie" value="UTF-8"/><input type="hidden" name="prev" value="_m"/><input type="text" name="q" style="width:65%" maxlength="2048" value="hello"/><input type="submit" value="Traduire"/></form><div class="small blue ub s2"><a href="http://translate.google.com/m?q=hello&amp;hl=fr&amp;sl=en&amp;tl=fr&amp;mui=sl" class="s1">Anglais</a><a id="arrow" href="http://translate.google.com/m?q=hello&amp;hl=fr&amp;sl=fr&amp;tl=en">&gt;</a><a href="http://translate.google.com/m?q=hello&amp;hl=fr&amp;sl=en&amp;tl=fr&amp;mui=tl" class="s1">Français</a></div><br><div dir="ltr" class="t0">Bonjour</div><form action="/m?hl=fr&amp;sl=en&amp;q=hello" class="blue ub db center"><div class="small nb s2 center"><a href="http://translate.google.com/m?q=hello&amp;hl=fr&amp;sl=en&amp;tl=fr&amp;mui=sl" class="s1">Anglais</a><a id="arrow" href="http://translate.google.com/m?q=hello&amp;hl=fr&amp;sl=fr&amp;tl=en">&gt;</a><a href="http://translate.google.com/m?q=hello&amp;hl=fr&amp;sl=en&amp;tl=fr&amp;mui=tl" class="s1">Français</a></div><input type="hidden" name="hl" value="fr"/><input type="hidden" name="sl" value="en"/><input type="hidden" name="tl" value="fr"/><input type="hidden" name="ie" value="UTF-8"/><input type="hidden" name="prev" value="_m"/><input type="text" name="q" style="width:65%" maxlength="2048" value="hello"/><input type="submit" value="Traduire"/></form><div class="small center"><br><br><a href="/m?hl=fr">Google Traduction - Page d&#39;accueil</a>&nbsp;-&nbsp;<a href="http://www.google.com/m?hl=fr">Accueil&nbsp;Google</a><br><br><a href="//www.google.com/tools/feedback/survey/xhtml?productId=95112&hl=fr">Envoyez-nous vos commentaires</a><br><br>Afficher Google version :<br><b>Mobile</b> |&nbsp;<a href="http://translate.google.com/?hl=fr&amp;sl=en&amp;vi=c">Classique</a><br><br>&copy;2017 Google&nbsp;-&nbsp;<a href="http://www.google.com/intl/fr/policies">Confidentialité et conditions d&#39;utilisation</a></div><script type="text/javascript">(new Image()).src="https://id.google.com/verify/ABGYjabvVTN-xZnuiknmEeXl6Vh9O2S_iGJzFP-bVzr8gRZb4FHdq5eNi5I9aPnXg80LHHywnylv2KY_E61jAqaSRCwYxiU5eNvAyKunzIW7dLw.gif";</script><noscript><img src="https://id.google.com/verify/ABGYjabvVTN-xZnuiknmEeXl6Vh9O2S_iGJzFP-bVzr8gRZb4FHdq5eNi5I9aPnXg80LHHywnylv2KY_E61jAqaSRCwYxiU5eNvAyKunzIW7dLw.gif" height=1 width=1 alt=""></noscript></body></html>'''

mock_session = MockSession(200, raw_html)
client = Translator(session=mock_session)

@pytest.mark.parametrize("text, expected", [
    ('this is a sample string with no punctuation', 31 ),
    ('thereisnoobvioussplitpoint',26),
    (' ',0),
    ('test.string',4)
])
def test_cutoff_point(text, expected):
    assert client._cutoff_point(text) == expected

@pytest.mark.parametrize("text, max_chunk_size, expected", [
    ('this is a sample string', 10, ['this is a', ' sample', ' string'] ),
    ('NoWayToSplitThisString', 5, ['NoWay', 'ToSpl', 'itThi', 'sStri', 'ng'] ),
    ('Nothing has really changed other than broadening of the spectrum of music that I listen to and dig for. Its also a bit easier to track stuff down with the internet now, but I still much prefer going to record stores, getting my fingers dirty and interacting with human beings-its more exciting that way',
     40, ['Nothing has really changed other than',
          ' broadening of the spectrum of music',
          ' that I listen to and dig for. Its also',
          ' a bit easier to track stuff down with',
          ' the internet now, but I still much',
          ' prefer going to record stores, getting',
          ' my fingers dirty and interacting with',
          ' human beings-its more exciting that',
          ' way'])
])
def test_split_request(text, max_chunk_size, expected):
    assert client._split_request(text, max_chunk_size) == expected


def test_split_request_proper_text_sizes():
    # ~ 20,000 characters of text
    sample_text = 10 * '''September 2005, the newspaper unveiled its newly designed front page, which debuted on Monday 12 September 2005. Designed by Mark Porter, the new look includes a new masthead for the newspaper, its first since 1988. The new format was generally well received by Guardian readers, who were encouraged to provide feedback on the changes. The only controversy was over the dropping of the Doonesbury cartoon strip. The paper reported thousands of calls and emails complaining about its loss; within 24 hours the decision was reversed and the strip was reinstated the following week. G2 supplement editor Ian Katz, who was responsible for dropping it, apologised in the editors' blog saying, "I'm sorry, once again, that I made you-and the hundreds of fellow fans who have called our helpline or mailed our comments' address-so cross."[153] However, some readers were dissatisfied as the earlier deadline needed for the all-colour sports section meant coverage of late-finishing evening football matches became less satisfactory in the editions supplied to some parts of the country. '''

    for chunk_size in [2000,4000,8000]:
        assert type(client._split_request(sample_text, chunk_size)) == list


def test_make_request():
    assert isinstance(client._make_request('http://example_url.com'),
                      MockResp) is True


@pytest.mark.parametrize("mock_resp, expected",[
                    (MockResp(text=''), ''),
                    (MockResp(text=raw_html),'Bonjour')]
                    )
def test_parse_content(mock_resp, expected): 
    assert client._parse_content(mock_resp) == expected


def test_construct_url():
    encoded_url = client._construct_url(text='hello mate',
                                 to_lang='fr',
                                 from_lang='en')
    assert type(encoded_url) == str
    assert encoded_url.startswith('http') is True



@pytest.mark.parametrize("text, chunk_size",[
                    ('short string', 500),
                    ('to be split up',7)]
                    )
def test_translate(text, chunk_size):
    assert isinstance(client.translate(text=text,
                        max_chunk_size=chunk_size),
                        string_types) is True
