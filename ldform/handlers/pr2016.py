import os
import json
import subprocess
from ..cgi import BASE_PATH, save, MyDict
from ..emailer import sendemail
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('ldform', 'templates'))

def respond(data):
    """Find talk data and edit them."""
    global BASE_PATH
    regid = os.path.basename(data.getfirst('r'))  # get rid of any slashes, etc
    nonce = data.getfirst('n')
    lang = data.getfirst('l', 'cs')
    action = data.getfirst('action')
    regfile = os.path.join(BASE_PATH, 'cfp2016', '{}.json'.format(regid))

    try:
        with open(regfile, 'r', encoding='utf-8') as inf:
            regdata = MyDict(json.load(inf))
        assert(regdata['nonce'] == nonce)
    except (IOError, AssertionError):
        raise RuntimeError('Cannot find such talk proposal.')


    if action == 'confirm' and not regdata.get('confirmed'):
        regdata['acconfirm'] = data['acconfirm']
        regdata['confirmed'] = True
        save(regdata)
        #Napsat e-mail hodymu
        email = 'orgs@linuxdays.cz'
        name = 'LinuxDays Orgs'
        emailtext = env.get_template('pr2016mail.j2').render(regdata=regdata)
        subject = "Potvrzení přihlášky na LinuxDays 2016"
        recipients = [(name, email)]
        sendemail(emailtext, subject, recipients)

        tplname = 'ack2016.j2' if lang == 'cs' else 'ack2016en.j2'
        tpl = env.get_template(tplname)
        print(tpl.render(regdata=regdata))
    else:
        tplname = 'pr2016.j2' if lang == 'cs' else 'pr2016en.j2'
        tpl = env.get_template(tplname)
        print(tpl.render(regdata=regdata))
