from setuptools import setup
setup(
  name = 'pygtranslate',
  packages = ['pygtranslate'],
  version = '0.0.1',
  description = 'Pythonic interface to google translate services',
  long_description = open('README.md').read(),
  long_description_content_type='text/markdown',
  author = 'Varun Balupuri',
  author_email = 'varunbalupuri@gmail.com',
  url = 'https://github.com/varunbalupuri/gtranslate-python',
  download_url = 'https://github.com/varunbalupuri/gtranslate-python/archive/0.1.tar.gz',
  keywords = ['translation', 'google translate', 'translate'], # arbitrary keywords
  classifiers = [],
  install_requires=['requests']
)
