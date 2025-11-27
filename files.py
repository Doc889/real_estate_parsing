import os
import shutil
import logging
import sys



# Root logger (только ваше приложение)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers.clear()

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)

# Telethon logger (выключаем)
telethon_logger = logging.getLogger("telethon")
telethon_logger.setLevel(logging.ERROR)
telethon_logger.propagate = False


async def save_media(message, unique_id):  # Function for saving the media files
    if message.media:
        os.makedirs("media", exist_ok=True)

        if message.photo:
            filename = f"media/{unique_id}.jpg"
        elif message.video:
            filename = f"media/{unique_id}.mp4"
        elif message.document:
            mime_type = message.document.mime_type
            ext = mime_type.split('/')[-1]
            filename = f"media/{unique_id}.{ext}"
        else:
            filename = f"media/{unique_id}"

        file_path = await message.download_media(file=filename)


async def delete_dir(message):
    folder = "media"

    try:
        shutil.rmtree(folder)  # Deleting media files
        logging.info(f"| MEDIA | {message} ")
    except Exception as e:
        logging.error(f"| MEDIA | Error cleaning media folder: {e}")


def delete_dir_sync():
    folder = "media"

    try:
        shutil.rmtree(folder, ignore_errors=True)
        print(f"| MEDIA | Media folder cleaned by shutdown handler")
    except Exception as e:
        print(f"| MEDIA | Error cleaning media folder on shutdown: {e}")
