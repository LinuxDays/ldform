from ..emailer import sendemail
import subprocess

notifytext = """
New registration on 3D-printing:

Name: {name[0]}
E-mail: {email[0]}
Phone: {phone[0]}
Company: {company[0]}
IC: {ic[0]}
Address: {address[0]}
Number of people: {person[0]}

Summary of all registrations can be obtained by issuing
/srv/www/ldform/export.py 3dt2015 name email phone company ic address lang person
"""

def respond(data):
    """Send e-mail notification"""
    email = 'miroslav.hroncok@fit.cvut.cz'
    name = 'Miro Hrončok'
    emailtext = notifytext.format_map(data)
    subject = "LinuxDays 2015 3D printing registration"
    recipients = [(name, email)]
    sendemail(emailtext, subject, recipients)

    print("Content-type: text/html; charset=UTF-8")
    print("""
<html>
<head>
    <meta http-equiv="refresh" content="10;/">
</head>
<body>
<h1>Your registration has been recorded.</h1>
<p>We will send you a reply soon.</p>
<p>Redirecting you <a href="/">back</a> in 10 seconds…</p>
</body>
</html>""")
