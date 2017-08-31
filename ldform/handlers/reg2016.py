from ..emailer import sendemail
import subprocess

notifytext = """
Děkujeme za registraci na LinuxDays. Ještě je potřeba registraci potvrdit.

Jméno: {name[0]}
Odebírat oznámení: {announces[0]}
Účast: {days[0]}
Oběd sobota: {mealsat[0]}
Oběd neděle: {mealsun[0]}

Svou registraci prosím potvrďte kliknutím na následující odkaz:
https://www.linuxdays.cz/cgi-bin/ldform.py?formid=conf2016&r={regid}&n={nonce}

Na stejném odkazu je možno registraci kdykoli později zrušit.

Děkujeme,
váš tým LinuxDays
"""

notifytexten = """
Thank you for registration to LinuxDays. You need to confirm it now.

Name: {name[0]}
Get announces: {announces[0]}
Days: {days[0]}
Meal Saturday: {mealsat[0]}
Meal Sunday: {mealsun[0]}

Please confirm your registration by clicking this link:
https://www.linuxdays.cz/cgi-bin/ldform.py?formid=conf2016&r={regid}&n={nonce}&l=en

You can also cancel your registration using the same link.

Thank You,
LinuxDays team
"""

def respond(data):
    """Send e-mail notification"""
    email = data.getfirst('email', '').strip()
    lang = data.getfirst('lang', 'cs').strip()
    data['confirmed'] = False
    data['validated'] = False
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

    print("Content-type: text/html; charset=UTF-8")
    if lang == 'cs':
        print("""
<html>
<head>
    <meta http-equiv="refresh" content="10;/">
</head>
<body>
<h1>Vaše registrace byla zaznamenána</h1>
<p>Registraci je nutné potvrdit v e-mailu, který byl odeslán na vaši adresu.</p>
<p>Přesměrujeme vás <a href="/">zpět</a> za 10 sekund…</p>
</body>
</html>""")
    else:
        print("""
<html>
<head>
    <meta http-equiv="refresh" content="10;/2016/en/">
</head>
<body>
<h1>Your registration has been recorded</h1>
<p>You need to confirm the registration by clicking the link in the e-mail you're just going to receive.</p>
<p>Redirecting you <a href="/2016/en/">back</a> in 10 seconds…</p>
</body>
</html>""")

