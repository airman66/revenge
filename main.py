import asyncio
from pyrogram import Client
from decouple import config
from pyrogram.enums import ChatAction
from datetime import datetime

api_id = config('API_ID')
api_hash = config('API_HASH')
phone = config('PHONE')
login = config('LOGIN')

user_id = config('USER_ID')

bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)

bot.start()

blocked = False

async def send_action():
    global blocked
    while True:
        if blocked:
            await bot.send_chat_action(user_id, ChatAction.TYPING)
            print(str(datetime.now()) + ": TYPING")
        await asyncio.sleep(1)

async def check_for_ban():
    global blocked
    while True:
        user = await bot.get_users(user_id)
        blocked = user.status.value == "long_ago"
        print(str(datetime.now()) + ": updated ban info, now it is " + str(blocked))
        await asyncio.sleep(10)

loop = asyncio.get_event_loop()
task1 = loop.create_task(send_action())
task2 = loop.create_task(check_for_ban())

try:
    loop.run_until_complete(asyncio.gather(task1, task2))
except asyncio.CancelledError:
    pass
finally:
    bot.stop()