from ..emailer import sendemail
import subprocess


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
    if '@' in email:
        name = data.getfirst('name', '')
        join_maillist(name, email, 'help2016', True)
    print("Content-type: text/html; charset=UTF-8")
    print("""
<html>
<head>
    <meta http-equiv="refresh" content="3;/">
</head>
<body>
<h1>Your response has been recorded. Thank you.</h1>
<p>Redirecting you <a href="/">back home</a> in 3 seconds…</p>
</body>
</html>
    """)
