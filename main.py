import email_handler
class Mail:
    def __init__(self, email_id, email, email_text, sender):
        self.mail_id = email_id
        self.email = email
        self.mail_text = email_text
        self.sender = sender
        self.classification = "unknown"
#   def email_classification(self): будет реализованно позже


for num in range(1, 101):
    email = email_handler.email_getter(num)
    email_sender = email_handler.get_sender(email)
    email_text = email_handler.get_text_email(email)
    email = Mail(num, email, email_text, email_sender)
