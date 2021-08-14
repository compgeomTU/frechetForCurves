from setuptools import setup, find_packages, Extension
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()
long_description = long_description.replace('![Image](/docs/', 'File unavailable: ')
long_description = long_description.replace('?raw=true)', '')
long_description = long_description.replace('[documentation.html](documentation.html)', 'documentation.html')
long_description = long_description.replace('[/docs](/docs)', '/docs')
