import logging
import random
import pickle
import time
import os

logging.basicConfig(format='\n[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

try:
    import vk_api
except ModuleNotFoundError:
    logging.critical('VK API pip module not found. Please install it before running this script.'); exit()

def send_message(vk, user_id, message):
    vk.messages.send(user_id=user_id, random_id=vk_api.utils.get_random_id(), message=message, attachment='wall-189698764_165')

if os.path.exists('vk_config.v2.json'):
    os.remove('vk_config.v2.json')

message_for_mailing = 'Привет, я тебе скину трек, если он тебе понравится, сможешь проявить активность в группе в качестве подписки или лайка ? А если тебе очень понравится, сможешь оформить подписочку, чтобы не пропустить самое интересное ? Примерно через 2 недели выйдет новый трек ☺ '

vk_app_id = '2685278'

while True:
    start_time = time.monotonic()

    accounts = []

    with open('accounts.txt') as file_accounts:
        for string_with_credentials in file_accounts:
            if string_with_credentials[0] != '#' and string_with_credentials.strip() != '':
                vk_login = string_with_credentials.split(':')[0].strip()
                vk_password = string_with_credentials.split(':')[1].strip()

                try:
                    vk_session = vk_api.VkApi(login=vk_login, password=vk_password, app_id=vk_app_id)
                    vk_session.auth()
                    vk = vk_session.get_api()
                except vk_api.exceptions.BadPassword:
                    logging.error(f'{vk_login}:{vk_password} Bad password!')
                except vk_api.exceptions.AuthError:
                    logging.error(f'{vk_login}:{vk_password} Authorization error! Account deactivated!')
                except vk_api.exceptions.Captcha:
                    pass
                else:
                    logging.info(f'{vk_login}:{vk_password} Successfully logged in!')
                    accounts.append(vk)

                time.sleep(5)

    print(f'Active accounts: {len(accounts)}')

    with open('users.txt', 'rb') as file_with_users:
        users_for_mailing = pickle.load(file_with_users)

    for times in range(random.randint(15, 30)):
        random.shuffle(users_for_mailing)

    for account in accounts:
        for user in range(19):
            try:
                send_message(account, users_for_mailing.pop(), message_for_mailing)
                logging.info(f'[https://vk.com/id{account._vk.token["user_id"]}] [{account._vk.login}:{account._vk.password}] Message sent!')
            except:
                logging.error(f'[https://vk.com/id{account._vk.token["user_id"]}] [{account._vk.login}:{account._vk.password}] Message cannot be sent!')
            time.sleep(10)

        logging.info(f'Mailing from account https://vk.com/id{account._vk.token["user_id"]} ({account._vk.login}:{account._vk.password}) completed!')

    print('Mailing completed!')

    with open('users.txt', 'wb') as file_users:
        pickle.dump(users_for_mailing, file_users)

    end_time = time.monotonic()

    logging.info(f'Sleep for {int(86400 - (end_time - start_time))} seconds...')
    time.sleep(86400 - (end_time - start_time))

    del(end_time, start_time)