import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate, formataddr, parseaddr
from email.header import Header
from sachima import conf

mail_host = conf.get("MAIL_HOST")
MAIL_ADD = conf.get("MAIL_ADD")
MAIL_USER = conf.get("MAIL_USER")
MAIL_PASS = conf.get("MAIL_PASS")
MAIL_SENDER = conf.get("MAIL_SENDER")


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


def send_mail(
    send_to, cc_to, subject, text, files=None, server=mail_host, ishtml=False
):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg["From"] = _format_addr(MAIL_SENDER + " <%s>" % MAIL_ADD)
    msg["To"] = COMMASPACE.join([_format_addr(x) for x in send_to])
    msg["CC"] = COMMASPACE.join([_format_addr(x) for x in cc_to])
    # msg['Date'] = formatdate(localtime=True)
    msg["Subject"] = subject

    if ishtml:
        msg.attach(MIMEText(text, "html", "utf-8"))
    else:
        msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                # Name=('gbk', '', basename(f))
                Name=basename(f),
            )
        # After the file is closed
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.login(MAIL_USER, MAIL_PASS)
    send_list = send_to + cc_to
    smtp.sendmail(MAIL_ADD, send_list, msg.as_string())
    smtp.close()
