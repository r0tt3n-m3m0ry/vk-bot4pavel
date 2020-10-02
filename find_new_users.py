try:
    import vk_api
except ModuleNotFoundError:
    print('VK API pip module not found. Please install it before running this script.'); exit()

import pickle

list_of_groups = [172831467, 149281650, 136483585, 125278260, 142163794, 173147726, 176686667, 157541471, 136478309, 150729800, 137046595, 122382351, 157681469, 142999382, 107359951, 108337741, 149737697, 160632532, 159536304, 156321274, 145617338, 173425827, 140370178, 163956083, 130686894, 125904625, 159659937, 158366559, 165993707, 157679819, 185109491, 49300993, 145640921, 166027814, 172242906, 123870813, 176374467, 155964596, 161404146]

users = []

valid_users = []

vk_login = input('VK login: ')
vk_password = input('VK password: ')

while True:
    try:
        vk_session = vk_api.VkApi(login=vk_login, password=vk_password)
        vk_session.auth()
        vk = vk_session.get_api()
    except vk_api.exceptions.BadPassword:
        print('Bad password!')
    except vk_api.exceptions.AuthError:
        print('Authorization error! Account deactivated!')
    else:
        print('Successfully logged in!')
        break

for group_id in list_of_groups:
    for offset in range(0, vk.groups.getMembers(group_id=group_id)['count'], 1000):
        for user_id in vk.groups.getMembers(group_id=group_id, count=1000, offset=offset)['items']:
            users.append(user_id)

for offset in range(0, len(users), 1000):
    for user in vk.users.get(user_ids=str(users[offset:offset+1000])[1:-1], fields='can_write_private_message, sex'):
        try:
            print(user['deactivated'])
        except KeyError:
            if user['can_write_private_message'] == 1 and user['sex'] == 1:
                valid_users.append(user['id'])
                print(user['id'])

for offset in range(0, len(valid_users), 19):
    print(valid_users[offset:offset+19])

with open('users.txt', 'wb') as file_users:
    pickle.dump(valid_users, file_users)