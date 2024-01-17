from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

SESSION_NAME = "channel_parser"
API_ID = 23988083
API_HASH = 'ffb67754a9b1261c067260958c870b04'
client = TelegramClient(SESSION_NAME, API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")
client.start()

def print_posts(chat):
    for message in client.iter_messages(chat):
        print(message.sender_id, ':', message.text)

async def get_history(channel):
	offset_msg = 0
	limit_msg = 5

	all_messages = []
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