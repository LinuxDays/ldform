#!/usr/bin/env python3

import email.mime.text
import email.utils
import email.header
import smtplib
import copy
import sys
import re
import argparse


def sendemail(textpart, subject, recipients,
              sender=("LinuxDays", "noreply@linuxdays.cz"),
              server="localhost"):
    """
    Send textual MIME e-mail
    @param textpart Textual part of e-mail
    @param subject Message subject
    @param recipients List of tuples of ("User Name", "E-mail address")
    @param sender Tuple of ("User Name", "E-mail address")
    @param server SMTP server
    """

    msgtpl = email.mime.text.MIMEText(textpart, _charset="utf-8")
    msgtpl['Subject'] = subject
    msgtpl['From'] = email.header.make_header(
        ((sender[0], None),
         ("<{}>".format(sender[1]), None))
    ).encode()
    msgtpl['Precedence'] = 'bulk'
    msgtpl['Date'] = email.utils.formatdate(localtime=True)

    smtp = smtplib.SMTP(server)
    for name, emailaddr in recipients:
        try:
            msg = copy.deepcopy(msgtpl)
            msg['Message-id'] = email.utils.make_msgid('linuxdays')
            msg['To'] = email.header.make_header(
                ((name, None),
                 ("<{}>".format(emailaddr), None))
            ).encode()
            # print(msg.as_string())
            smtp.send_message(msg)
        except:
            print("Unexpected error:", sys.exc_info()[0])
    smtp.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LinuxDays spammer')
    parser.add_argument('--subject', "-s", help='message Subject',
                        default='LinuxDays informace')
    parser.add_argument('--fromname', help='sender name', default='LinuxDays')
    parser.add_argument('--fromemail', '-f', help='sender e-mail',
                        default='noreply@linuxdays.cz')
    parser.add_argument('recipients', help='file with recipient list, one'
                        'on line, formatted Jmeno Prijmeni <adresa>',)
    parser.add_argument('text', help='file with message body',)
    parser.add_argument('--notest', help='actually send the messages',
                        action='store_true')

    args = parser.parse_args()

    recipients = list()
    with open(args.recipients) as recfile:
        for line in recfile:
            m = re.match('(.*) <([^>]*)>$', line)
            if m:
                recipients.append(m.groups())

    print("{} recipients added...".format(len(recipients)))
    with open(args.text) as bodyfile:
        textpart = bodyfile.read()

    if args.notest:
        print("Sending...")
        sendemail(textpart, args.subject, recipients,
                  (args.fromname, args.fromemail))
    else:
        print(
            "About to send text:\n{}\nfrom:{} <{}>\n"
            "with subject: {}\nto addresses:{}".format(
                textpart, args.fromname, args.fromemail,
                args.subject, recipients
            )
        )
