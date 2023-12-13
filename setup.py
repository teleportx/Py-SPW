from os import path, environ

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    description_md = f.read()

requirements = open('requirements.txt', 'r').read().split('\n')

exec(sorted([el if el.startswith('__version__') else 'Z' for el in open('./pyspw/__init__.py', 'r').read().split('\n')], reverse=True)[0])

if environ.get('version') is not None:
    __version__ = environ.get('version')

setup(
    name='Py-SPW',
    version=__version__,
    packages=['pyspw'],
    url='https://github.com/teleportx/Py-SPW',
    license='MIT License',
    author='Stepan Khozhempo',
    author_email='stepan@xstl.ru',
    description='Python library for spworlds API',
    long_description=description_md,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    python_requires='>=3.7',
    project_urls={
        "Docs": "https://pyspw.xstl.ru/en/latest/",
        "GitHub": "https://github.com/teleport2/Py-SPW/"
    },
)
