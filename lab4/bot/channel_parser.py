from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from settings import SESSION_NAME, API_ID, API_HASH

client = TelegramClient(SESSION_NAME, API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")
client.start()

def print_posts(chat):
    for message in client.iter_messages(chat):
        print(message.sender_id, ':', message.text)

async def get_history(channel):
	# номер записи, с которой начинается считывание
	offset_msg = 0

	# максимальное число записей, передаваемых за один раз
	limit_msg = 5   

	# список всех сообщений
	all_messages = []

	# поменяйте это значение, если вам нужны не все сообщения
	total_count_limit = 5  

	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, 
			add_offset=0,
			limit=limit_msg, 
			max_id=0, 
			min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			data = message.to_dict()
			all_messages.append({
				'id': data['id'],
				'text': data['message']
            })

			if len(all_messages) >= total_count_limit:
				return all_messages

	return all_messages