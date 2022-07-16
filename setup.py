from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    description_md = f.read()

requires = ['requests==2.28.1']

setup(
    name='Py-SPW',
    version='1.1',
    packages=['pyspw'],
    url='https://github.com/teleport2/Py-SPW',
    license='MIT License',
    author='Stepan Khozhempo',
    author_email='stepan@m.khoz.ru',
    description='Python library for spworlds API',
    long_description=description_md,
    long_description_content_type='text/markdown'
)
