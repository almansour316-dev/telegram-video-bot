
import logging
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from yt_dlp import YoutubeDL, DownloadError

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TOKEN = "7708762018:AAFfUU3TZi92uUIFUOz6fteuMt3DJOJH8IU"
DOWNLOAD_DIR = "./downloads"
COOKIES_FILE = "cookies.txt"

# Create download directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def start(update: Update, context) -> None:
    """Sends a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"مرحباً {user.mention_html()}!\nأنا بوت تحميل الفيديوهات. أرسل لي رابط فيديو وسأقوم بتحميله لك."
    )

async def download_video(update: Update, context) -> None:
    """Downloads a video from a given URL and sends it to the user."""
    url = update.message.text
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=chat_id, text="جاري التحميل...")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'progress_hooks': [lambda d: download_progress_hook(d, update, context)],
    }

    # Add cookies support if cookies.txt exists
    if os.path.exists(COOKIES_FILE):
        ydl_opts['cookiefile'] = COOKIES_FILE
        logger.info(f"Using cookies from {COOKIES_FILE}")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
        os.remove(file_path) # Clean up the downloaded file

    except DownloadError as e:
        error_message = str(e)
        user_friendly_message = "حدث خطأ أثناء تحميل الفيديو: "

        if "Instagram" in url and ("login" in error_message or "private" in error_message or "restricted" in error_message):
            user_friendly_message += "هذا المنشور يتطلب تسجيل دخول أو أنه خاص. يرجى توفير ملف cookies.txt لتسجيل الدخول." 
        elif "No appropriate format found" in error_message:
            user_friendly_message += "لم يتم العثور على تنسيق مناسب للفيديو. قد يكون الفيديو غير متاح أو يتطلب تنسيقًا خاصًا." 
        else:
            user_friendly_message += f"فشل التحميل. السبب: {error_message}"
        
        logger.error(f"DownloadError: {error_message}")
        await context.bot.send_message(chat_id=chat_id, text=user_friendly_message)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await context.bot.send_message(chat_id=chat_id, text=f"حدث خطأ غير متوقع أثناء تحميل الفيديو: {e}")

def download_progress_hook(d, update: Update, context) -> None:
    """Progress hook for yt-dlp to send updates to the user."""
    if d['status'] == 'downloading':
        # You can add more detailed progress updates here if needed
        pass
    elif d['status'] == 'finished':
        logger.info(f"Finished downloading: {d['filename']}")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
