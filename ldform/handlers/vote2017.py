import os
import re
import json
import collections
from ..cgi import BASE_PATH, save, MyDict
from ..emailer import sendemail
import markdown
from jinja2 import Environment, Markup, PackageLoader

md = markdown.Markdown(extensions=['markdown.extensions.nl2br'],
                       output_format='xhtml5')
env = Environment(loader=PackageLoader('ldform', 'templates'))
env.filters['markdown'] = lambda text: Markup(md.convert(text))


def respond(data):
    """Show ballot summary."""
    email = data.getfirst('confemail')
    if email and '@' in email:
        lang = data.getfirst('lang', 'cs')
        tplname = 'voteconfmail.j2' if lang == 'cs' else 'voteconfmailen.j2'
        emailtext = env.get_template(tplname).render(data=data)
        subject = "LinuxDays: potvrzení hlasování" if lang == 'cs' else "LinuxDays: vote confirmation"
        recipients = [('', email.strip())]
        sendemail(emailtext, subject, recipients)

    print("""Status: 303 See Other
Location: /cgi-bin/ldform.py?formid=vote2017conf&b={}
Content-type: text/html; charset=UTF-8")

<html>
<body>
<h1>Your response has been recorded. Thank you.</h1>
</body>
</html>
""".format(data['regid']))
