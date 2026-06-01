def email_getter(num_of_mail):
    email_file = open(f'inbox/mail_{"0" * (4-len(str(num_of_mail))) + str(num_of_mail)}.txt', 'r', encoding="utf-8")
    return email_file

def get_sender(full_email):
    first_line = full_email.readline().strip()
    if "To:" in first_line:
        return first_line.split("To: ")[1]
    elif "От кого:" in first_line:
        return first_line.split("От кого: ")[1]

def get_text_email(full_email):
    return "".join(full_email.readlines()[4:])

