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


def findcfp(regid, base='cfp2017'):
    """Load CfP data. Fail silently"""
    regfile = os.path.join(BASE_PATH, base, '{}.json'.format(regid))
    try:
        with open(regfile, 'r', encoding='utf-8') as inf:
            regdata = MyDict(json.load(inf))
    except (IOError):
        regdata = MyDict()
    return regdata

def validregid(regid):
    m = re.match('20[0-9]{2}(0[1-9]|1[0-2])[0-3][0-9]-[0-2][0-9]'
                 '([0-5][0-9]){2}-[a-z]{3}', regid)
    return m is not None


def respond(data):
    """Show ballot summary."""
    global BASE_PATH
    ballotid = os.path.basename(data.getfirst('b'))  # get rid of any slashes, etc
    ballotfile = os.path.join(BASE_PATH, 'vote2017', '{}.json'.format(ballotid))

    try:
        with open(ballotfile, 'r', encoding='utf-8') as inf:
            data = MyDict(json.load(inf))
    except (IOError, AssertionError):
        raise RuntimeError('Cannot find such ballot.')

    votes = []
    Vote = collections.namedtuple('Vote', 'regdata, points')
    for k, v in data.items():
        if not validregid(k):
            continue
        regdata = findcfp(k);
        votes.append(Vote(regdata, v))

    votes = reversed(sorted(votes, key=lambda v: v.points))
    lang = data.getfirst('lang', 'cs')
    tplname = 'voteconfirm.j2' if lang == 'cs' else 'voteconfirmen.j2'
    tpl = env.get_template(tplname)
    print(tpl.render(votes=votes, data=data))
