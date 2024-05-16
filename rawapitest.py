import asyncio
import aiohttp

TOKEN='7012513939:AAGHf4-DSqK9D70av_Vnw-8ADcq5zQ99XiE'

URL = f'https://api.telegram.org/bot{TOKEN}/'

async def send_message(chat_id, text):
    async with aiohttp.ClientSession() as session:
        params = {'chat_id': chat_id, 'text': text}
        async with session.post(URL + 'sendMessage', data=params) as response:
            await response.json()

async def handle_updates(update):
    message = update.get('message' , False)
    if message:
        chan_id = message['chat_id'][id]
        text = message.get('text', False)

        if text:
            await send_message(chat_id, f'Эхо {text}')
        else:
            await send_message(chan_id, 'Я працюю тільки з текстом')

async def get_updates():
    offset = None
                                
    