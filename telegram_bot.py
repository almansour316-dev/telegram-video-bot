import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from yt_dlp import YoutubeDL, DownloadError

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")
COOKIES_FILE = os.getenv("COOKIES_FILE", "cookies.txt")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def start(update: Update, context) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"مرحباً {user.mention_html()}!\nأنا بوت تحميل الفيديوهات. أرسل لي رابط فيديو وسأقوم بتحميله لك."
    )


async def download_video(update: Update, context) -> None:
    url = (update.message.text or "").strip()
    chat_id = update.effective_chat.id
    file_path = None

    if not url.startswith(("http://", "https://")):
        await context.bot.send_message(chat_id=chat_id, text="أرسل رابط فيديو صالح يبدأ بـ http أو https")
        return

    await context.bot.send_message(chat_id=chat_id, text="جاري التحميل...")

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s-%(title).80s.%(ext)s"),
        "noplaylist": True,
        "restrictfilenames": True,
    }

    if os.path.exists(COOKIES_FILE):
        ydl_opts["cookiefile"] = COOKIES_FILE
        logger.info("Using configured cookies file")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        with open(file_path, "rb") as document:
            await context.bot.send_document(chat_id=chat_id, document=document)

    except DownloadError as exc:
        logger.warning("Video download failed: %s", exc)
        await context.bot.send_message(
            chat_id=chat_id,
            text="تعذر تحميل الفيديو. تأكد من أن الرابط عام ومتاح ثم حاول مرة أخرى.",
        )
    except Exception:
        logger.exception("Unexpected download error")
        await context.bot.send_message(
            chat_id=chat_id,
            text="حدث خطأ غير متوقع أثناء معالجة الفيديو.",
        )
    finally:
        if file_path and os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except OSError:
                logger.warning("Could not remove temporary file: %s", file_path)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is required")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
