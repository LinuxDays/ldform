import os
import json
import subprocess
from ..cgi import BASE_PATH

confirmationtext = """Content-type: text/html; charset=UTF-8

<html>
<body>
<h1>Prosím potvrďte zrušení registrace</h1>
<form action="/cgi-bin/ldform.py" method="post">
<input type=hidden name="formid" value="unreg2015">
<input type=hidden name="r" value="{r[0]}">
<input type=hidden name="n" value="{n[0]}">
<input type=hidden name="confirm" value="yes">
<input type=submit value="Zrušit registraci">
</form>
</body>
</html>
"""

removaltext = """Content-type: text/html; charset=UTF-8

<html>
<head>
    <meta http-equiv="refresh" content="3;/">
</head>
<body>
<h1>Vaše registrace byla zrušena</h1>
<p>Přesměrujeme vás <a href="/">zpět</a> za 3 sekundy…</p>
</body>
</html>
"""


def leave_maillist(email, listname):
    cmd = ['sudo', '/usr/sbin/remove_members', '-f', '-',
           listname]
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    ps.communicate(email.encode('utf-8'))


def respond(data):
    """Find registration data and delete them."""
    global BASE_PATH
    regid = os.path.basename(data.getfirst('r'))  # get rid of any slashes, etc
    nonce = data.getfirst('n')
    confirm = data.getfirst('confirm')
    regfile = os.path.join(BASE_PATH, 'reg2015', '{}.json'.format(regid))

    try:
        with open(regfile, 'r', encoding='utf-8') as inf:
            regdata = json.load(inf)
        assert(regdata['nonce'] == nonce)
    except (IOError, AssertionError):
        raise RuntimeError('Cannot find such registration.')

    if confirm == 'yes':
        if regdata.get('announces', ['no'])[0] == 'yes':
            leave_maillist(regdata.get('email', [''])[0], 'announce2015')
        os.remove(regfile)
        print(removaltext)
    else:
        print(confirmationtext.format_map(data))
