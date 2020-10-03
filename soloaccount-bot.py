import logging
import time
import os

logging.basicConfig(format='\n[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

try:
    import vk_api
except ModuleNotFoundError:
    logging.critical('VK API pip module not found. Please install it before running this script.'); exit()

def send_message(user_id, message):
    vk.messages.send(user_id=user_id, random_id=vk_api.utils.get_random_id(), message=message, attachment='wall-189698764_9')

if os.path.exists('vk_config.v2.json'):
    os.remove('vk_config.v2.json')

messages_for_mailing = ['Привет, я тебе скину трек, если он тебе понравится, сможешь проявить активность в группе в качестве подписки или лайка ? А если тебе очень понравится, сможешь оформить подписочку, чтобы не пропустить самое интересное ? Примерно через 2 недели выйдет новый трек ☺ ']
users_for_mailing = []

vk_login = input('VK login: ')
vk_password = input('VK password: ')

vk_app_id = '2685278'

while True:
    try:
        vk_session = vk_api.VkApi(login=vk_login, password=vk_password, app_id=vk_app_id)
        vk_session.auth()
        vk = vk_session.get_api()
    except vk_api.exceptions.BadPassword:
        logging.error('Bad password!')
    except vk_api.exceptions.AuthError:
        logging.error('Authorization error! Account deactivated!')
    else:
        logging.info('Successfully logged in!')
        break

if len(users_for_mailing) == 0:
    print('Enter user_id\'s for mail him or list with user_id\'s. User must be opened for income messages from you account. If not, this will be reported in the console and his account will be deleted from mailing list.\n\nIf you enter all user_id\'s, enter just 0.')

    while True:
        user_id = input(f'USER_ID ({len(users_for_mailing)+1}) : ')

        if user_id[0] == '[' and user_id[-1] == ']':
            for user_id_from_list in user_id[1:-1].split(','):
                users_for_mailing.append(user_id_from_list.strip())
        else:
            if user_id != '0':
                users_for_mailing.append(user_id)
            else:
                break

if len(messages_for_mailing) == 0:
    print('Enter messagess for mail them or list with messages. For send attachment, start message from symbor \'@\', and after write attachment in VK attachments format. If you enter all messagess, enter just 0.')

    while True:
        message = input(f'MESSAGE ({len(messages_for_mailing)+1}) : ')

        if message[0] == '[' and message[-1] == ']':
            for message_from_list in message[1:-1].split(','):
                messages_for_mailing.append(message_from_list.strip())
        else:
            if message != '0':
                messages_for_mailing.append(message)
            else:
                break

for message in messages_for_mailing:
    for user_id in users_for_mailing:
        try:
            send_message(user_id, message)
            logging.info(f'Message sent!')
        except:
            logging.info(f'Message cannot be sent!')
        time.sleep(10)

logging.info('Mailing completed!')