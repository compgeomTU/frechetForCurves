from distutils.core import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
  name = 'pyfrechet',
  packages = ['pyfrechet'],
  version = '0.1',
  license='MIT',
  description = 'Frechet Distance Python Library',
  author = 'Will Rodman',
  author_email = 'wrodman@tulane.edu',
  url = 'https://github.com/compgeomTU/frechetForCurves',
  download_url = 'https://github.com/compgeomTU/frechetForCurves/archive/refs/tags/0.1.tar.gz',
  package_dir = {'': 'src/'},
  long_description=long_description,
  long_description_content_type='text/markdown',
  install_requires=[
          'numpy',
          'matplotlib',
          'shapely',
          'cffi'
      ],
  classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9'
    ]
)
