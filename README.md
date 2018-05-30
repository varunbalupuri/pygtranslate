# gtranslate-python

Pythonic interface with CLI to Google's free Translate API.

## Features:
* Supports request splitting for large requests (>4000 chars default) to circumvent `GET` char limit. Requests will be split on end of sentences preferably to preserve quality of translation.
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

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details