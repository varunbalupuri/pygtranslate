# pygtranslate

Pythonic interface with CLI to Google's free Translate API for python 2.7 and 3.x

## Features:
* Supports request splitting for large requests (>4000 chars default) to circumvent `GET` char limit. Large translation requests will be split on end of sentences where possible to preserve quality of translation.
* Proxy support via `HTTPS_PROXY` environment variable.
* Agent spoofing.
* Uses google's auto language detection where possible by default if not explicitly specified.

## Usage:
```
client = Translator()
client.translate('Bonjour', from_lang='fr', to_lang='en')
>>> 'Hello'
```

## Command Line tool:
```
python translator.py -t en -f fr -q "Bonjour"
>>> Hello
```

## Installation

The easiest way is with pip:
```
pip install pygtranslate
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.txt) file for details.