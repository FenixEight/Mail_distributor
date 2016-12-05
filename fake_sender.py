import time
import random


class FakeSenderError(Exception):
    pass


def send_email(from_name, from_email, to_email, subject, body_text, body_html):
    time.sleep(1)
    if random.randint(1, 10) == 5:
        raise FakeSenderError('Unable to send an email.')
    print 'Email has been sent to ', to_email
