try:
	import vk_api
except ModuleNotFoundError:
	print('VK API pip module not found. Please install it before running this script.'); exit()

import time

count_of_active_accounts = 0

with open('accounts.txt') as file_accounts:
	for line_with_credentials in file_accounts:
		if line_with_credentials[0] != '#':
			vk_login = line_with_credentials.split(':')[0].strip()
			vk_password = line_with_credentials.split(':')[-1].strip()

			try:
				vk_session = vk_api.VkApi(login=vk_login, password=vk_password)
				vk_session.auth()
				vk = vk_session.get_api()
			except vk_api.exceptions.BadPassword:
				print(f'{vk_login}:{vk_password} Bad password!')
			except vk_api.exceptions.AuthError:
				print(f'{vk_login}:{vk_password} Authorization error! Account deactivated!')
			else:
				print(f'{vk_login}:{vk_password} Successfully logged in!')

			count_of_active_accounts += 1

			time.sleep(10)

print(f'Active accounts: {count_of_active_accounts}')