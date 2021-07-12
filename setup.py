import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '1.0'
PACKAGE_NAME = 'pyfrechet'
AUTHOR = 'Will Rodman'
AUTHOR_EMAIL = 'wrodman@tulane.edu'
URL = 'https://github.com/compgeomTU/frechetForCurves'

LICENSE = 'MIT License'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ['geopandas']

setup(name=PACKAGE_NAME,
      version=VERSION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
