# Py SPW
Library for work with [SPWorlds](https://spworlds.ru) API in Python.

## Installation
Need python version >=3.7

```shell
pip install Py-Spw
```

## Quick start
*Checking user access*
```python
import pyspw

api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')

print(api.check_access('437610383310716930'))
```

### How to
You can see [examples](https://github.com/teleportx/Py-SPW/tree/main/examples) to help solve your problem

## Links
- [PyPi](https://pypi.org/project/Py-SPW)
- [Documentation](https://github.com/teleportx/Py-SPW/wiki)
- [API](https://github.com/sp-worlds/api-docs)