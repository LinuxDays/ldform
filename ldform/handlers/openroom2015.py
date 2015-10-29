from ..emailer import sendemail
import subprocess

notifytext = """
Nová přihláška na OpenRoom:

Jméno: {name[0]}
E-mail: {email[0]}
Telefon: {phone[0]}
Den: {day[0]}
Čas: {from[0]} - {to[0]}
Název: {title[0]}
Popis: {abstract[0]}
Veřejné: {open[0]}

Výpis všech registrací je k nalezení příkazem
/srv/www/ldform/export.py openroom2015 name email phone day from to public title abstract
"""

def respond(data):
    """Send e-mail notification"""
    email = 'openroom@linuxdays.cz'
    name = 'OpenRoom admin'
    emailtext = notifytext.format_map(data)
    subject = "LinuxDays 2015 OpenRoom požadavek"
    recipients = [(name, email)]
    sendemail(emailtext, subject, recipients)

    print("Content-type: text/html; charset=UTF-8")
    print("""
<html>
<head>
    <meta http-equiv="refresh" content="10;/">
</head>
<body>
<h1>Vaše registrace byla zaznamenána</h1>
<p>Vyčkejte prosím na potvrzení rezervace od týmu LinuxDays.</p>
<p>Přesměrujeme vás <a href="/">zpět</a> za 10 sekund…</p>
</body>
</html>""")
