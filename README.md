[![PyPI version](https://badge.fury.io/py/Py-SPW.svg)](https://pyspw.xstl.ru/ru/latest/?badge=latest)
[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](https://pyspw.xstl.ru/ru/latest/?badge=latest)

[![Documentation Status](https://readthedocs.org/projects/py-spw/badge/?version=latest)](https://pyspw.xstl.ru/ru/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/teleportx/Py-SPW/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/Py-SPW)](https://pyspw.xstl.ru/ru/latest/?badge=latest)

# Py SPW
Library for work with [SPWorlds](https://spworlds.ru) API in Python.

## Installation
**You need python >=3.7**

```shell
pip install Py-SPW
```

## Getting example
*Checking user access*
```python
import pyspw

api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')

print(api.check_access('437610383310716930'))
```

## Ask help

* See the code [examples](https://github.com/teleportx/Py-SPW/tree/main/examples)
* If you found a bug in a library report it to [issue tracker](https://github.com/teleportx/Py-SPW/issues)
* Get help with your code using Py-SPW [discussions](https://github.com/teleportx/Py-SPW/discussions)


## Links
- [PyPi](https://pypi.org/project/Py-SPW)
- [Documentation](https://pyspw.xstl.ru/en/latest/)
- [API](https://github.com/sp-worlds/api-docs)
