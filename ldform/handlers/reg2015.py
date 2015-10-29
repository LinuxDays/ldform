from ..emailer import sendemail
import subprocess

notifytext = """
Děkujeme za registraci na LinuxDays.

Jméno: {name[0]}
Odebírat oznámení: {announces[0]}
Účast: {days[0]}

Budete-li chtít svou registraci zrušit, použijte následující odkaz:
https://www.linuxdays.cz/cgi-bin/ldform.py?formid=unreg2015&r={regid}&n={nonce}

Děkujeme,
váš tým LinuxDays
"""

notifytexten = """
Thank you for registration to LinuxDays.

Name: {name[0]}
Get announces: {announces[0]}
Days: {days[0]}

Should you cancel your registration, follow this link:
https://www.linuxdays.cz/cgi-bin/ldform.py?formid=unreg2015&r={regid}&n={nonce}

Thank You,
LinuxDays team
"""

def join_maillist(name, email, listname, welcome=False):
    stdin = "{} <{}>".format(name, email).encode('utf-8')
    cmd = ['sudo', '/usr/sbin/add_members', '-r', '-',
           '-w', 'y' if welcome else 'n', '-a', 'n', listname]
    env = {'LANG': 'en_US.UTF-8'}
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE, env=env)
    ps.communicate(stdin)


def respond(data):
    """Send e-mail notification"""
    email = data.getfirst('email', '').strip()
    lang = data.getfirst('lang', 'cs').strip()
    if '@' in email:
        name = data.getfirst('name', '')
        if lang == 'cs':
            emailtext = notifytext.format_map(data)
            subject = "LinuxDays registrace"
        else:
            emailtext = notifytexten.format_map(data)
            subject = "LinuxDays registration"
        recipients = [(name, email)]
        sendemail(emailtext, subject, recipients)
        if data.getfirst('announces', 'no') == 'yes':
            join_maillist(name, email, 'announce2015')
        if data.getfirst('talk', 'no') == 'yes':
            join_maillist(name, email, 'talk2015', True)

    print("Content-type: text/html; charset=UTF-8")
    if lang == 'cs':
        print("""
<html>
<head>
    <meta http-equiv="refresh" content="3;/">
</head>
<body>
<h1>Vaše registrace byla zaznamenána</h1>
<p>Přesměrujeme vás <a href="/">zpět</a> za 3 sekundy…</p>
</body>
</html>""")
    else:
        print("""
<html>
<head>
    <meta http-equiv="refresh" content="3;/2015/en/">
</head>
<body>
<h1>Your registration has been recorded</h1>
<p>Redirecting you <a href="/2015/en/">back</a> in 3 seconds…</p>
</body>
</html>""")

