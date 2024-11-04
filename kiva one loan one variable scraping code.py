# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#clean code to scrap one variable from one loan on kiva
import requests
base_url = 'https://api.kivaws.org/graphql?query='
graphql_query = "{lend {loan (id: 1568001){id name}}}"
r = requests.get(base_url+ graphql_query)
r.json()

#messy code demonstrating we are trying to solve an "expecting value" error and a "Response 403" eror.
Python 3.12.7 | packaged by Anaconda, Inc. | (main, Oct  4 2024, 13:17:27) [MSC v.1929 64 bit (AMD64)]
Type "copyright", "credits" or "license" for more information.

IPython 8.27.0 -- An enhanced Interactive Python.

# this snippet requires the requests library which can be installed
# via pip with the command: pip install requests
pip install requests
import requests

base_url = 'https://api.kivaws.org/graphql?query='

graphql_query = "{lend {loan (id: 1568001){id name}}}"

r = requests.get(base_url+ graphql_query )
r.json()
  Cell In[1], line 3
    pip install requests
        ^
SyntaxError: invalid syntax


import requests

base_url = 'https://api.kivaws.org/graphql?query='

graphql_query = "{lend {loan (id: 1568001){id name}}}"

r = requests.get(base_url+ graphql_query)

r
Out[6]: <Response [403]>

r.json()
Traceback (most recent call last):

  File ~\AppData\Local\anaconda3\Lib\site-packages\requests\models.py:974 in json
    return complexjson.loads(self.text, **kwargs)

  File ~\AppData\Local\anaconda3\Lib\json\__init__.py:346 in loads
    return _default_decoder.decode(s)

  File ~\AppData\Local\anaconda3\Lib\json\decoder.py:337 in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())

  File ~\AppData\Local\anaconda3\Lib\json\decoder.py:355 in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None

JSONDecodeError: Expecting value


During handling of the above exception, another exception occurred:

Traceback (most recent call last):

  Cell In[7], line 1
    r.json()

  File ~\AppData\Local\anaconda3\Lib\site-packages\requests\models.py:978 in json
    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)

JSONDecodeError: Expecting value


r = requests.get(base_url+ graphql_query)

base_url+ graphql_query
Out[9]: 'https://api.kivaws.org/graphql?query={lend {loan (id: 1568001){id name}}}'

r = requests.get(base_url+ graphql_query)

r
Out[11]: <Response [403]>

graphql_query
Out[12]: '{lend {loan (id: 1568001){id name}}}'

graphql_query = "{lend {loan (id: 156800){id name}}}"

r = requests.get(base_url+ graphql_query)

r
Out[15]: <Response [403]>

graphql_query = "{lend {loan (id: 1568002){id name}}}"

r = requests.get(base_url+ graphql_query)

r
Out[18]: <Response [403]>

graphql_query = "{lend {loan (id: 1568001){id name}}}"



graphql_query
Out[20]: '{lend {loan (id: 1568001){id name}}}'

base_url+ graphql_query
Out[21]: 'https://api.kivaws.org/graphql?query={lend {loan (id: 1568001){id name}}}'

r = requests.get(base_url+ graphql_query)

r
Out[23]: <Response [403]>

r = requests.post(base_url+ graphql_query)

r
Out[25]: <Response [403]>

r.json()
Traceback (most recent call last):

  File ~\AppData\Local\anaconda3\Lib\site-packages\requests\models.py:974 in json
    return complexjson.loads(self.text, **kwargs)

  File ~\AppData\Local\anaconda3\Lib\json\__init__.py:346 in loads
    return _default_decoder.decode(s)

  File ~\AppData\Local\anaconda3\Lib\json\decoder.py:337 in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())

  File ~\AppData\Local\anaconda3\Lib\json\decoder.py:355 in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None

JSONDecodeError: Expecting value


During handling of the above exception, another exception occurred:

Traceback (most recent call last):

  Cell In[26], line 1
    r.json()

  File ~\AppData\Local\anaconda3\Lib\site-packages\requests\models.py:978 in json
    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)

JSONDecodeError: Expecting value

