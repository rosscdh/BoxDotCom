from distutils.core import setup
from setuptools import find_packages

setup(
    name='boxdotcom',
    version='0.1.0',
    author="Ross Crawford-d'Heureuse",
    author_email='ross@lawpal.com',
    packages=['boxdotcom'],
    include_package_data=True,
    url='https://github.com/rosscdh/BoxDotComApi',
    description='Module for interacting with the BoxDotCom v2 api',
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=[
        'WTForms',
        'requests',
        'nose',
        'python-oauth2',
        'querystring-parser',
        'mocktest'
     ]
)
