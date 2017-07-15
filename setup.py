import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'flask',
    'requests',
    'ujson'
]


setup(name='teams_bot',
      version='0.0',
      description='teams_bot',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
      ],
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )
