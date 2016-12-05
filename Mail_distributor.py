import logging
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from ServerHelper import *
from fake_sender import send_email, FakeSenderError

logging.basicConfig(format='%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO, filename='log.txt')
STATUS = None


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/', '/RPC2')


def send_newsletter(newsletter, users):
    if STATUS.get_status() == 'ready':
        logging.info('Start sending')
        letter, users_list = unpack(newsletter, users)
        start_thread(letter, users_list)


def send(newsletter, users):
    STATUS.set_status('sending')
    dump(newsletter, 'letter')
    STATUS.total = len(users)
    for user in users:
        if not user.sent and STATUS.get_status() == 'sending':
            try:
                dump(users, 'users')
                send_email(newsletter.from_name, newsletter.from_email, user.email,
                           newsletter.subject, newsletter.body_text, newsletter.body_html)
                user.sent = True

                STATUS.status_obj.last_id = user.user_id
                STATUS.sent += 1
                logging.info('Email has been sent to ' + user.email + ' id: ' + str(user.user_id))
                if STATUS.total == STATUS.sent:
                    logging.info('finished')
                    STATUS.set_status('stopped')
                    reset()
            except FakeSenderError as err:
                logging.error('Error sending:' + user.email + ' id: ' + str(user.user_id))
                STATUS.status_obj.error = err.message + 'id:' + str(user.user_id)
                STATUS.set_status('sending_error')


def start_thread(newsletter, users):
    thread = threading.Thread(target=send, args=(newsletter, users,))
    thread.start()


def resume():
    if STATUS.status_obj.status != 'ready':
        logging.info('Resume')
        users = undump('users')
        letter = undump('letter')
        STATUS.count_sent(users)
        start_thread(letter, users)


def stop():
    if STATUS.status_obj.status != 'ready':
        logging.info('stopped')
        STATUS.set_status('stopped')


def reset():
    if STATUS.get_status() == 'stopped' or STATUS.get_status() == 'sending_error':
        logging.info('Reset')
        clear_dumps()
        STATUS.set_status('ready')
        STATUS.status_obj.last_id = None
        STATUS.sent = 0
        STATUS.status_obj.error = None


def get_state():
    return STATUS.status_obj


server = SimpleXMLRPCServer(("localhost", 8000), logRequests=True, allow_none=True)
server.register_function(send_newsletter, 'send_newsletter')
server.register_function(resume, 'resume')
server.register_function(reset, 'reset')
server.register_function(stop, 'stop')
server.register_function(get_state, 'get_state')
STATUS = StatusHelper()
server.serve_forever()
