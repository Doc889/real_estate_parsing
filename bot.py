from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile, InputMediaPhoto, InputMediaVideo

import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("bot_token")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def send_media_from_folder(chat_id: int, folder_path: str, text: str):  # Function for sending post to user
    files = sorted(
        [f for f in os.listdir(folder_path) if
         f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))])  # Getting array of media files
    if not files:
        print("No media.")
        return

    media = []
    for i, file_name in enumerate(files):
        file_path = os.path.join(folder_path, file_name)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        ext = os.path.splitext(file_name)[1].lower()

        if ext in ('.jpg', '.jpeg', '.png'):
            media_type = InputMediaPhoto
        elif ext in ('.mp4', '.mov'):
            media_type = InputMediaVideo
        else:
            continue

        file = FSInputFile(file_path)
        media.append(media_type(media=file, caption=text if i == 0 else None))

    await bot.send_media_group(chat_id=chat_id, media=media)
    await bot.session.close()

# asyncio.run(send_media_from_folder(chat_id=965153930/378020258, folder_path="media", text="Описание альбома"))
