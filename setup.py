
from os import path

from setuptools import find_packages
from setuptools import setup


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django-testbox',
    version='0.0.2',
    description='Testing tools for Django projects',
    long_description=long_description,
    url='https://github.com/mtirsel/django-testbox',
    author='Martin Tiršel',
    author_email='martin.tirsel@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='django testing development',
    packages=find_packages(),
    install_requires=['django', 'selenium']
)
