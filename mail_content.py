import re


class MailContent:

    def __init__(self, subject, sender, content):
        self.subject = subject
        self.sender = sender
        self.content = content


    @classmethod
    def mail_from_text(self, text):
        parts = text.split('\n')
        subject = parts[0]
        text = "\n".join(parts[1:])

        parts = re.split(r"\n\n", text)

        if len(parts) < 3:
            return None

        return MailContent(subject, parts[0], "\n\n".join(parts[1:]))