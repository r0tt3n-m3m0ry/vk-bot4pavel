try:
    import vk_api
except ModuleNotFoundError:
    print('VK API pip module not found. Please install it before running this script.'); exit()

from datetime import datetime
import random
import pickle
import time

def send_message(vk, user_id, message):
    vk.messages.send(user_id=user_id, random_id=vk_api.utils.get_random_id(), message=message, attachment='wall-189698764_9')

message_for_mailing = 'Привет, я тебе скину трек, если он тебе понравится, сможешь проявить активность в группе в качестве подписки или лайка ? А если тебе очень понравится, сможешь оформить подписочку, чтобы не пропустить самое интересное ? Примерно через 2 недели выйдет новый трек ☺ '

accounts = []

vk_app_id = '2685278'

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
                print('Bad password!')
            except vk_api.exceptions.AuthError:
                print('Authorization error! Account deactivated!')
            else:
                print('Successfully logged in!')
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
            print(f'[{datetime.now().strftime("%H:%M:%S")}] Message sent!')
        except:
            print(f'[{datetime.now().strftime("%H:%M:%S")}] Message cannot be sent!')
        time.sleep(10)

print('Mailing completed!')

with open('users.txt', 'wb') as file_users:
    pickle.dump(users_for_mailing, file_users)