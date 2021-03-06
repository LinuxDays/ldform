from ..emailer import sendemail
import subprocess

notifytext = """
Nový CfP odeslán:

Typ: {type[0]}
Název: {title[0]}
Obtížnost: {difficulty[0]}
Délka: {time[0]}
OpenAlt: {openalt[0]}
Jméno: {name[0]}
E-mail: {email[0]}
Telefon: {phone[0]}
Twitter: {twitter[0]}
Tričko: {tshirt[0]}
Den: {day[0]}
Party: {social[0]}

Abstrakt:
{abstract[0]}

Další vzkazy:
{remarks[0]}

Výpis všech registrací je k nalezení příkazem:
$ /home/ldform/ldform/export.py cfp2016 type title difficulty time openalt abstract name email phone twitter tshirt device day accomodation social remarks
"""

def respond(data):
    """Send e-mail notification"""
    email = 'orgs@linuxdays.cz'
    name = 'LinuxDays Orgs'
    emailtext = notifytext.format_map(data)
    subject = "Nové CfP pro LinuxDays 2016"
    recipients = [(name, email)]
    sendemail(emailtext, subject, recipients)

    print("Content-type: text/html; charset=UTF-8")
    print("""
<html>
<head>
    <meta http-equiv="refresh" content="10;/">
</head>
<body>
<h1>Your response has been recorded. Thank you.</h1>
<p>Redirecting you <a href="/">back home</a> in 3 seconds…</p>
</body>
</html>""")
