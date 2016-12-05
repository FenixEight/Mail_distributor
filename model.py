class User:
    def __init__(self, user_id, full_name, email):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.sent = False


class Newsletter:
    def __init__(self, newsletter_id, newsletter_name, from_name, from_email,
                 subject, body_text, body_html):
        self.newsletter_id = newsletter_id
        self.newsletter_name = newsletter_name
        self.from_name = from_name
        self.from_email = from_email
        self.subject = subject
        self.body_text = body_text
        self.body_html = body_html


class Status:
    def __init__(self):
        self.last_id = None
        self.status = None
        self.error = None