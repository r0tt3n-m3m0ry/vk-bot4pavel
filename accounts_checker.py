try:
	import vk_api
except ModuleNotFoundError:
	print('VK API pip module not found. Please install it before running this script.'); exit()

import time

file_headers = ['# All credentials must be in format vk_login:vk_pass', '# For example, 89999999999:qwerty123', '# Lines with \'#\' in the start of string will be ignored', '# Created by @r0tt3n-m3m0ry for Pavel Bocharov (Matteo), 2020\n']

accounts = []

count_of_active_accounts = 0

with open('accounts.txt') as file_accounts:
	for line_with_credentials in file_accounts:
		if line_with_credentials[0] != '#' and line_with_credentials.strip() != '' and ':' in line_with_credentials:
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

				accounts.append(f'{vk_login}:{vk_password}')

				time.sleep(5)

print(f'Active accounts: {count_of_active_accounts}')

with open('accounts.txt', 'w') as file_accounts:
	for header in file_headers:
		file_accounts.write(header + '\n')

	for account in accounts:
		file_accounts.write(account + '\n')