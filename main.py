from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client
import json

# Reads files content
with open('config/config.json', 'r') as config_json:
    data_json = json.loads(config_json.read())

with open('config/text.txt', 'r') as config_txt:
    data_txt = config_txt.read()

app = Client("bot", data_json["api_id"], data_json["api_hash"])

# Function to send message in chats
async def job():

    for i in data_json["chats_to_spam"]:

        await app.send_photo(chat_id=i, photo=f'config/{data_json["photo_name"]}', caption=data_txt)

# Launches job every 2 hours
try:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", minutes=120)
    scheduler.start()
    app.run()
except:
    scheduler.shutdown()
    app.stop()