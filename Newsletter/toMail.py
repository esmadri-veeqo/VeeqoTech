from appscript import app, k
from mactypes import Alias

def get_html_with_css_as_string(name):
    with open('./Templates/%s.html' % name, 'r') as html_file:
        html = html_file.read()
    with open('./Templates/%s.css' % name, 'r') as css_file:
        css = css_file.read()
        html_with_css = html.replace('<link rel="stylesheet" type="text/css" href="%s.css"/>'% name, '<style>\n%s\n</style>'% css)
    return html_with_css

def create_message(name, subject, to_recip):
    body = get_html_with_css_as_string(name)
    msg = Message(subject=subject, body=body, to_recip=to_recip, show_=False)
    msg.send()

class Outlook(object):
    def __init__(self):
        self.client = app('Microsoft Outlook')

class Message(object):
    def __init__(self, parent=None, subject='', body='', to_recip=[], cc_recip=[], show_=True):

        if parent is None: parent = Outlook()
        client = parent.client

        self.msg = client.make(
            new=k.outgoing_message,
            with_properties={k.subject: subject, k.content: body})

        self.add_recipients(emails=to_recip, type_='to')
        self.add_recipients(emails=cc_recip, type_='cc')

        if show_: self.show()

    def show(self):
        self.msg.open()
        self.msg.activate()

    def send(self):
        self.msg.send()

    def add_attachment(self, p):
        # p is a Path() obj, could also pass string

        p = Alias(str(p)) # convert string/path obj to POSIX/mactypes path

        attach = self.msg.make(new=k.attachment, with_properties={k.file: p})

    def add_recipients(self, emails, type_='to'):
        if not isinstance(emails, list): emails = [emails]
        for email in emails:
            self.add_recipient(email=email, type_=type_)

    def add_recipient(self, email, type_='to'):
        msg = self.msg

        if type_ == 'to':
            recipient = k.to_recipient
        elif type_ == 'cc':
            recipient = k.cc_recipient

        msg.make(new=recipient, with_properties={k.email_address: {k.address: email}})


create_message(
    "DataTypes",
    "Ruby Essentials: Data Types",
    ["esmadri@veeqo.com"]
)