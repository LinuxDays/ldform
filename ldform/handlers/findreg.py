import os
import json
import re
from ..cgi import BASE_PATH
from ..cgi import MyDict

confirmationtext = """Content-type: text/html; charset=UTF-8

<html>
<body>
<h1>Nalezení registrace</h1>
<form action="/cgi-bin/ldform.py" method="get">
<input type="hidden" name="formid" value="findreg">
<input type="text" name="q" placeholder="Hledané jméno" value="{q}">
<input type="submit">
</form>
<table>
<tr><th>#</th><th>Jméno</th><th>regid</th></tr>
{table}
</table>
</body>
</html>
"""



def respond(data):
    """Find registration data and delete them."""
    global BASE_PATH
    query = data.getfirst('q', '')
    path = os.path.join(BASE_PATH, 'reg2015')
    order = 0
    results = []
    if len(query) > 2:
        for f in sorted(os.listdir(path)):
            if not f.endswith('.json'):
                continue
            with open(os.path.join(path, f), 'r', encoding='utf-8') as inf:
                data = MyDict(json.load(inf))
            order += 1
            name = data.getfirst('name')
            if not name:
                continue
            regid = data.get('regid')
            if re.search(query, name, re.I):
                results.append((order, name, regid))

    rows = ("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(o, n, r) 
             for o, n, r in results)
    table = "\n".join(rows)
    print(confirmationtext.format(q=query, table=table))
