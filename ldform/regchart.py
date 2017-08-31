#!/usr/bin/env python3
import os
import json
import sys
from collections import defaultdict
from datetime import datetime

from gviz_api import DataTable
from cgi import MyDict

from pprint import pprint
BASE_PATH = '/home/ldform/lddata'
OUT_PATH = '/var/www/linuxdays.cz/2016/grafy/'

def regidtodate(regid):
    return datetime(int(regid[:4]), int(regid[4:6]), int(regid[6:8]),
                    int(regid[9:11]), int(regid[11:13]),
                    int(regid[13:15]))

def main(formid='reg2016'):
    """ Generate list of with values for *args. """
    global BASE_PATH
    events = []
    counts = defaultdict(int)
    meals_sat = defaultdict(int)
    meals_sun = defaultdict(int)
    path = os.path.join(BASE_PATH, formid)
    for f in sorted(os.listdir(path)):
        if not f.endswith('.json'):
            continue
        with open(os.path.join(path, f), 'r', encoding='utf-8') as inf:
            data = MyDict(json.load(inf))
        regdate = regidtodate(data.get('regid'))
        events.append((regdate, 1, 0, 0, 1))
        if data.get('confirmed'):
            confdate = regidtodate(data.get('confirmed_by_regid'))
            events.append((confdate, 0, 1, 0, 0))
            validate = regidtodate(data.get('validated_by_regid'))
            events.append((validate, 0, 0, 0, -1))
            days = data.getfirst('days')
            if days in ['sat', 'both']:
                counts['sat'] += 1
            if days in ['sun', 'both']:
                counts['sun'] += 1
            m_sat = data.getfirst('mealsat')
            if m_sat:
                meals_sat[m_sat] += 1
            m_sun = data.getfirst('mealsun')
            if m_sun:
                meals_sun[m_sun] += 1
            if ':' in data.get('ip'):
                counts['ipv6'] += 1
            else:
                counts['ipv4'] += 1
            if data.getfirst('bastlirna') == 'yes':
                counts['bastlirna'] += 1
            if data.getfirst('gentoo') == 'yes':
                counts['gentoo'] += 1
            if data.getfirst('lang') == 'en':
                counts['en'] += 1
            if data.getfirst('prefilled') == 'true':
                counts['prefilled'] += 1
        elif data.get('validated'):
            confdate = regidtodate(data.get('confirmed_by_regid'))
            events.append((confdate, 0, 1, 0, 0))
            cancdate = regidtodate(data.get('cancelled_by_regid'))
            events.append((cancdate, 0, -1, 1, 0))
            validate = regidtodate(data.get('validated_by_regid'))
            events.append((validate, 0, 0, 0, -1))

    events2 = []
    lastrec = (None, 0, 0, 0, 0)
    for r in sorted(events):
        if lastrec[0] == r[0]:
            events2.pop()
            lastrec = (r[0], r[1]+lastrec[1], r[2]+lastrec[2], r[3]+lastrec[3], r[4]+lastrec[4])
        else:
            lastrec = r
        events2.append(lastrec)

    countchartdata = []
    for d, cnt, conf, canc, nonv in events2:
        counts['all'] += cnt
        counts['confirmed'] += conf
        counts['cancelled'] += canc
        counts['invalid'] += nonv
        countchartdata.append({"date": d, "count": counts['all'],
                               "confirmed": counts['confirmed'],
                               "cancelled": counts['cancelled'],
                               "invalid": counts['invalid']})


    with open(os.path.join(OUT_PATH, 'stats.json'), 'w') as outf:
        json.dump(counts, outf)

    with open(os.path.join(OUT_PATH, '..', 'count.txt'), 'w') as outf:
        outf.write("linuxdays_registrace {}\n".format(counts['confirmed']))

    with open(os.path.join(OUT_PATH, 'regdate.json'), 'wb') as outf:
        t = DataTable({"date": ("datetime", "Datum"),
                       "count": ("number", "Celkem"),
                       "confirmed": ("number", "Potvrzené"),
                       "cancelled": ("number", "Zrušené"),
                       "invalid": ("number", "Nepotvrzené"),
                       })
        t.LoadData(countchartdata)
        outdata = t.ToJSon(columns_order=("date", "count", "confirmed",
                                          "invalid", "cancelled"),
                                    order_by="date")
        outf.write(outdata)

    with open(os.path.join(OUT_PATH, 'regdays.json'), 'wb') as outf:
        t = DataTable({"day": ("string", "Den"),
                       "count": ("number", "Počet registrací")})
        t.LoadData([{"day": "Sobota", "count": counts['sat']},
                    {"day": "Neděle", "count": counts['sun']},
                    {"day": "Gentoo Miniconf", "count": counts['gentoo']},
        #            {"day": "Bastlírna pro děti", "count": counts['bastlirna']},
                    {"day": "Anglické registrace", "count": counts['en']}])
        outdata = t.ToJSon(columns_order=("day", "count"))
        outf.write(outdata)

    with open(os.path.join(OUT_PATH, 'mealsat.json'), 'wb') as outf:
        t = DataTable({"name": ("string", "Menu"),
                       "count": ("number", "Počet porcí")})
        meals = ["Menu 1",
                 "Menu 2",
                 "Menu 3"]
        t.LoadData([{"name": meals[0], "count": meals_sat['menu1']},
                    {"name": meals[1], "count": meals_sat['menu2']},
                    {"name": meals[2], "count": meals_sat['menu3']},])
        outdata = t.ToJSon(columns_order=("name", "count"))
        outf.write(outdata)

    with open(os.path.join(OUT_PATH, 'mealsun.json'), 'wb') as outf:
        t = DataTable({"name": ("string", "Menu"),
                       "count": ("number", "Počet porcí")})
        meals = ["Menu 1",
                 "Menu 2",
                 "Menu 3"]
        t.LoadData([{"name": meals[0], "count": meals_sun['menu1']},
                    {"name": meals[1], "count": meals_sun['menu2']},
                    {"name": meals[2], "count": meals_sun['menu3']},])
        outdata = t.ToJSon(columns_order=("name", "count"))
        outf.write(outdata)

    with open(os.path.join(OUT_PATH, 'regip.json'), 'wb') as outf:
        t = DataTable({"proto": ("string", "Protokol"),
                       "count": ("number", "Počet registrací")})
        t.LoadData([{"proto": "IPv4", "count": counts['ipv4']},
                    {"proto": "IPv6", "count": counts['ipv6']}])
        outdata = t.ToJSon(columns_order=("proto", "count"))
        outf.write(outdata)

def party(formid='party2015'):
    """ Generate list of with values for *args. """
    global BASE_PATH
    meals = defaultdict(int)
    path = os.path.join(BASE_PATH, formid)
    for f in sorted(os.listdir(path)):
        if not f.endswith('.json'):
            continue
        with open(os.path.join(path, f), 'r', encoding='utf-8') as inf:
            data = MyDict(json.load(inf))
        m = data.getfirst('meal')
        if m:
            meals[m] += 1

    with open('/srv/www/web/2015/party/meals.json', 'wb') as outf:
        t = DataTable({"name": ("string", "Menu"),
                       "count": ("number", "Počet porcí")})
        mealnames = ["Marinovaná krkovička v pikantní marinádě s chilli, česnekem a zázvorem a arašídovým olejem, podávaná s grilovaným ananasem, dýní a bramborovými klínky",
                     "Pečená vepřová žebra marinovaná v třtinovém cukru, chilli, limetce, podávaná s domácím pečivem",
                     "1/4 pečené kachny s červeným a bílým zelím podávaná s houskovým a bramborovým knedlíkem",
                     "Kuřecí křidélka v pikantní BBQ omáčce s rozpečenou bagetou, zeleninovým crudité a domácí sýrovou omáčkou",
                     "Fusilli s pancettou, kuřecím masem, sušenými rajčaty, česnekem, cibulí a oreganem, sypané parmezánem",
                     "Domácí bramborové gnocchi se špenátem a hříbky, sypané parmezánem"]
        t.LoadData([{"name": mealnames[i], "count": meals['meal%d'%i]} for i in range(1,6)])
        outdata = t.ToJSon(columns_order=("name", "count"))
        outf.write(outdata)

if __name__ == '__main__':
    main()
    #party()
