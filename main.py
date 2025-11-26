from telethon import TelegramClient
from dotenv import load_dotenv

import logging
import os
import asyncio
import shutil
import sys

from db_functions import *
from bot import send_media_from_folder
from extraction import check_text
from files import save_media, delete_dir

load_dotenv()

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
channels = [
    'https://t.me/arenduzb',
    'https://t.me/arenda_in_tashkent',
    'https://t.me/dom_arenda_kvartira',
    'https://t.me/arentash',
    'https://t.me/kvartira_dom_arenda',
    'https://t.me/tashkentkvartiraarenda'
]

# Root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

folder = "media"

client = TelegramClient('session', int(api_id), api_hash)


async def main():
    logging.info("| DATABASE | Initializing database...")
    await db_init()  # Initializing db

    logging.info("| TELEGRAM | Starting Telegram client...")
    await client.start()  # Starting the client

    while True:
        arr = await get_data_from_db()  # Getting ids of old posts
        message_ids = [i[1] for i in arr]
        logging.info(f"| DATABASE | Loaded {len(message_ids)} existing message IDs from DB.")

        for channel in channels:
            entity = await client.get_entity(channel)  # Getting telegram channel
            logging.info(f"| TELEGRAM | Processing channel: {channel}")

            async for message in client.iter_messages(entity, limit=100):  # Post's iterating
                unique_id = f"{message.chat_id}_{message.id}"  # Initializing the unique id
                logging.info(f"| TELEGRAM | Processing message {unique_id} | Date: {message.date}")

                await save_media(message, unique_id)  # Save the media files

                if message.text:
                    logging.info(f"| MEDIA | Media saved for message {unique_id}")
                    if unique_id not in message_ids:  # Check either the post has been already sent
                        try:
                            valid_post = await check_text(message.text)  # Validating of new posts
                            logging.info(f"| VALIDATING | Validating new post {unique_id}...")
                        except Exception as e:
                            logging.error(f"| VALIDATING | Error validating post {unique_id}: {e}")
                            continue

                        if valid_post:  # If post is validated
                            try:
                                await insert_db(unique_id)  # Adding the unique_id of new post in db
                                logging.info(f"Post {unique_id} inserted into DB.")
                                await send_media_from_folder(
                                    chat_id=378020258,
                                    folder_path="media",
                                    text=message.text
                                )  # Sending the post to user
                                logging.info(f"| TELEGRAM BOT | Post {unique_id} sent to user.")
                            except Exception as e:
                                logging.error(f"| TELEGRAM BOT | Error sending post {unique_id}: {e}")

                    await delete_dir("Media folder cleaned for next post.")
                    await asyncio.sleep(1)  # Delay between messages

            await delete_dir(f"Media of {channel} has been cleaned")
            await asyncio.sleep(5)  # Delay between channels

        logging.info("| LOOP | Starting next full cycle in 60 seconds...")
        await asyncio.sleep(60)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program has been stopped.")
finally:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print("Folder media has been deleted.")
