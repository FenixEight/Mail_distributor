import os

from model import *
import cPickle as pickle


class StatusHelper:
    def __init__(self):
        self.status_obj = Status()
        if len(self.get_status()) == 0:
            self.set_status('ready')
        self.status_obj.status = self.get_status()
        self.status_obj.last_id = None
        self.status_obj.error = None
        self.total = None
        self.sent = 0

    def get_status(self):
        f = open('status.txt', 'r')
        status = f.read()
        f.close()
        return status

    def set_status(self, status):
        f = open('status.txt', 'w')
        f.write(status)
        f.close()
        self.status_obj.status = status

    def count_sent(self, users):
        count = 0
        for u in users:
            if u.sent:
                count += 1
        self.sent = count
        self.total = len(users)


def unpack(newsletter, users):
    letter = Newsletter(newsletter['newsletter_id'], newsletter['newsletter_name'],
                        newsletter['from_name'], newsletter['from_email'], newsletter['subject'],
                        newsletter['body_text'], newsletter['body_html'])
    users_list = []
    for user in users:
        u = User(user['user_id'], user['full_name'], user['email'])
        users_list.append(u)
    return letter, users_list


def dump(item, target):
    output = open(target + '.pkl', 'wb')
    pickle.dump(item, output, 2)
    output.close()


def undump(target):
    i = open(target + '.pkl', 'rb')
    item = pickle.load(i)
    i.close()
    return item


def clear_dumps():
    os.remove('users.pkl')
    os.remove('letter.pkl')
