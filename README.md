[![PyPI version](https://badge.fury.io/py/Py-SPW.svg)](https://pypi.org/project/Py-SPW/)
[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](https://pypi.org/project/Py-SPW/)

[![Documentation Status](https://github.com/teleportx/Py-SPW/actions/workflows/docs-publish.yml/badge.svg)](https://pyspw.xstl.ru/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/teleportx/Py-SPW/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/Py-SPW)](https://pypi.org/project/Py-SPW/)

**Follow [telegram channel](https://t.me/xstl_devblog) to receive a notification about new version.**

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
- [Documentation](https://pyspw.xstl.ru/)
- [API](https://github.com/sp-worlds/api-docs)
