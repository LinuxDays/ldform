import os
import json
import subprocess
from ..cgi import BASE_PATH, save

confirmationtext = """Content-type: text/html; charset=UTF-8

<html>
<body>
<h1>Vaše registrace</h1>
<pre>
Jméno: {name[0]}
E-mail: {email[0]}
Odebírat oznámení: {announces[0]}
Účast: {days[0]}
Oběd sobota: {mealsat[0]}
Oběd neděle: {mealsun[0]}
</pre>

<form action="/cgi-bin/ldform.py" method="post">
<input type=hidden name="formid" value="conf2016">
<input type=hidden name="r" value="{r[0]}">
<input type=hidden name="n" value="{n[0]}">
"""


nonconfirmedtext = """
<p>Registrace dosud <strong>není potvrzena</strong>.</p>
<input type=hidden name="action" value="confirm">
<input type=submit value="Potvrdit registraci">
</form>
</body>
</html>
"""

confirmedtext = """
<p>Registrace <strong>je potvrzena</strong>.</p>
<input type=hidden name="action" value="cancel">
<input type=submit value="Zrušit registraci">
</form>
</body>
</html>
"""

removaltext = """Content-type: text/html; charset=UTF-8

<html>
<head>
    <meta http-equiv="refresh" content="10;/">
</head>
<body>
<h1>Vaše registrace byla zrušena, děkujeme.</h1>
<p>Pokud si svou neúčast rozmyslíte, můžete registraci znovu potvrdit
odkazem v původním e-mailu.</p>
<p>Přesměrujeme vás <a href="/">zpět</a> za 10 sekund…</p>
</body>
</html>
"""

confirmaltext = """Content-type: text/html; charset=UTF-8

<html>
<head>
    <meta http-equiv="refresh" content="3;/">
</head>
<body>
<h1>Vaše registrace byla potvrzena, děkujeme.</h1>
<p>Přesměrujeme vás <a href="/">zpět</a> za 3 sekundy…</p>
</body>
</html>
"""

confirmationtexten = """Content-type: text/html; charset=UTF-8

<html>
<body>
<h1>Your registration</h1>
<pre>
Name: {name[0]}
E-mail: {email[0]}
Announces: {announces[0]}
Attendance: {days[0]}
Meal Saturday: {mealsat[0]}
Meal Sunday: {mealsun[0]}
</pre>

<form action="/cgi-bin/ldform.py" method="post">
<input type=hidden name="formid" value="conf2016">
<input type=hidden name="l" value="en">
<input type=hidden name="r" value="{r[0]}">
<input type=hidden name="n" value="{n[0]}">
"""


nonconfirmedtexten = """
<p>Registration is <strong>not yet confirmed</strong>.</p>
<input type=hidden name="action" value="confirm">
<input type=submit value="Confirm registration">
</form>
</body>
</html>
"""

confirmedtexten = """
<p>Registration <strong>is confirmed</strong>.</p>
<input type=hidden name="action" value="cancel">
<input type=submit value="Cancel registration">
</form>
</body>
</html>
"""

removaltexten = """Content-type: text/html; charset=UTF-8

<html>
<head>
    <meta http-equiv="refresh" content="10;/2016/en/">
</head>
<body>
<h1>Your registration has been canceled. Thank you.</h1>
<p>You can re-confirm your registration by using the same confirmation link.</p>
<p>Redirecting you <a href="/2016/en/">back</a> in 10 seconds…</p>
</body>
</html>
"""

confirmaltexten = """Content-type: text/html; charset=UTF-8

<html>
<head>
    <meta http-equiv="refresh" content="3;/2016/en/">
</head>
<body>
<h1>Your registration has been confirmed. Thank you.</h1>
<p>Redirecting you <a href="/2016/en/">back</a> in 3 seconds…</p>
</body>
</html>
"""

def join_maillist(name, email, listname, welcome=False):
    stdin = "{} <{}>".format(name, email).encode('utf-8')
    cmd = ['sudo', '/usr/sbin/add_members', '-r', '-',
           '-w', 'y' if welcome else 'n', '-a', 'n', listname]
    env = {'LANG': 'en_US.UTF-8'}
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE, env=env)
    ps.communicate(stdin)


def leave_maillist(email, listname):
    cmd = ['sudo', '/usr/sbin/remove_members', '-f', '-',
           listname]
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    ps.communicate(email.encode('utf-8'))


def respond(data):
    """Find registration data and edit them."""
    global BASE_PATH
    regid = os.path.basename(data.getfirst('r'))  # get rid of any slashes, etc
    nonce = data.getfirst('n')
    lang = data.getfirst('l', 'cs')
    action = data.getfirst('action')
    regfile = os.path.join(BASE_PATH, 'reg2016', '{}.json'.format(regid))

    try:
        with open(regfile, 'r', encoding='utf-8') as inf:
            regdata = json.load(inf)
        assert(regdata['nonce'] == nonce)
    except (IOError, AssertionError):
        raise RuntimeError('Cannot find such registration.')

    if action == 'cancel' and regdata.get('confirmed') == True:
        #if regdata.get('announces', ['no'])[0] == 'yes':
        #    leave_maillist(regdata.get('email', [''])[0], 'announce')
        if regdata.get('confirmed'):
            regdata['cancelled_by_regid'] = data['regid']
            regdata['confirmed'] = False
        save(regdata)
        print(removaltext if lang == 'cs' else removaltexten)

    elif action == 'confirm' and regdata.get('confirmed') == False:
        if regdata.get('announces', ['no'])[0] == 'yes':
            join_maillist(regdata['name'][0], regdata['email'][0], 'announce')
        if regdata.get('talk', ['no'])[0] == 'yes':
            join_maillist(regdata['name'][0], regdata['email'][0], 'talk', True)
        if not regdata.get('confirmed'):
            regdata['confirmed'] = True
            regdata['confirmed_by_regid'] = data['regid']
        if not regdata.get('validated'):
            regdata['validated'] = True
            regdata['validated_by_regid'] = data['regid']
        save(regdata)
        print(confirmaltext if lang == 'cs' else confirmaltexten)

    else:
        data.update(regdata)
        txt = confirmationtext if lang == 'cs' else confirmationtexten
        print(txt.format_map(data))
        if regdata['confirmed']:
            print(confirmedtext if lang == 'cs' else confirmedtexten)
        else:
            print(nonconfirmedtext if lang == 'cs' else nonconfirmedtexten)
