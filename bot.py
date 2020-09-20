try:
    import vk_api
except ModuleNotFoundError:
    print('VK API pip module not found. Please install it before running this script.'); exit()

import pickle

def get_vk_name(vk, user_id): # return vk first and last names of owner user_id
    first_name = vk.users.get(user_ids=user_id)['first_name']
    last_name = vk.users.get(user_ids=user_id)['last_name']
    return list(first_name, last_name)

def find_new_users(vk, list_of_groups): # create pickle dump with users ids - groups members
    users = {}

    for group_id in list_of_groups:
        for offset in range(0, vk.groups.getMembers(group_id=group_id)['count'], 1000):
            for user_id in vk.groups.getMembers(group_id=gruoup_id, count=1000, offset=offset)['items']:
                try:
                    print(vk.users.get(user_ids=user_id))[0]['deactivated']
                except KeyError:
                    if vk.users.get(user_ids=user_id, fields='can_write_private_message')['can_write_private_message'] == 1:
                        users[user_id] = 0

    with open('users.txt', 'wb') as file_users:
        pickle.dump(users, file_users)

def send_message(vk, user_id, message):
    vk.messages.send(user_id=user_id, random_id=vk_api.utils.get_random_id(), message=message)

messages_for_spaming = ['1', '2', '3']

try:
    with open('users.txt', 'rb') as file_users:
        users_for_spamming = pickle.load(file_users)
except FileNotFoundError:
    print('First run this script with \'-i\' flag and call find_new_users for filling file with user_ids'); exit()

accounts = {}

with open('accounts.txt') as file_accounts:
    for account_credentials in file_accounts:
        vk_login = account_credentials.split(':')[0]
        vk_password = account_credentials.split(':')[1]

        try:
            vk_session = vk_api.VkApi(login=vk_login, password=vk_password, app_id='2685278') # app_id from kate mobile for vk_api messages bypass
            vk_session.auth()
        except vk_api.exceptions.BadPassword:
            print(f'Account {vk_login}:{vk_password} - Bad Password. Ignored.')
            continue
        except vk_api.exceptions.AuthError:
            print(f'Account {vk_login}:{vk_password} - Authorization Error. Ignored.')
            continue
        else:
            print(f'Account {vk_login}:{vk_password} - Successful logged in!')
            vk = vk_session.get_api()
            accounts[vk] = 0

print(f'Active accounts: {len(accounts)}')
