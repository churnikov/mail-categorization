import imaplib
import pyzmail.parse as pyzm


class MailCrawler(object):
    """
    Iterates over mail from mail server over imap.
    """

    def __init__(self, host, mail_address, password, port):
        self.mail_addr = mail_address
        self.host = host
        self.password = password
        self.SMPT_PORT = port
        self.mail = imaplib.IMAP4_SSL(self.host)

    def connect(self):
        """
        Connects to mail server. If something wrong happens, raise ConnectionError.
        """
        try:
            self.mail.login(self.mail_addr, self.password)
        except:
            raise ConnectionError('Unable to connect to mail server')

    def disconnect(self):
        """
        Logout from mail server.  If something wrong happens, raise ConnectionError.
        """
        try:
            self.mail.logout()
        except:
            raise ConnectionError('Can\'t log out or already logout')

    def get_mail(self):
        """
        Generator for mail of PyzMessage type.
        :return:
            yields PyzMessage object.
        """
        self.mail.select('inbox', readonly=True)
        type, data = self.mail.uid('search', None, 'All')
        mail_ids = data[0]
        id_list = mail_ids.split()

        for i in id_list:
            result, data = self.mail.uid('fetch', i, '(RFC822)')
            yield pyzm.PyzMessage(pyzm.PyzMessage.smart_parser(data[0][1]))

    def get_text(self):
        """
        Generator for text from emails.
        :return:
            yields string text
        """
        for message in self.get_mail():
            text = []
            for mailpart in message.mailparts:
                if mailpart.is_body == 'text/plain':
                    text.append(pyzm.decode_text(mailpart.get_payload(), mailpart.charset, None)[0])
            yield '\n'.join(text)
