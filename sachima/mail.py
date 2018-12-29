import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate, formataddr, parseaddr
from email.header import Header
import yaml

with open('conf/sachima.yaml') as f:
    c = yaml.load(f)
    mail_host = c['mail']['mail_host']
    mail_add = c['mail']['mail_add']
    mail_user = c['mail']['mail_user']
    mail_pass = c['mail']['mail_pass']
    mail_sender = c['mail']['mail_sender']


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(send_to, cc_to, subject, text, files=None,
              server=mail_host, ishtml=False):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = _format_addr(mail_sender+' <%s>' % mail_add)
    msg['To'] = COMMASPACE.join([_format_addr(x) for x in send_to])
    msg['CC'] = COMMASPACE.join([_format_addr(x) for x in cc_to])
    # msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    if ishtml:
        msg.attach(MIMEText(text, 'html', 'utf-8'))
    else:
        msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                # Name=('gbk', '', basename(f))
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.login(mail_user, mail_pass)
    send_list = send_to + cc_to
    smtp.sendmail(mail_add, send_list, msg.as_string())
    smtp.close()
