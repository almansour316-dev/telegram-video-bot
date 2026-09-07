# Telegram Video Bot

بوت تيليجرام بسيط لتحميل الفيديوهات باستخدام `yt-dlp`.

## التشغيل

1. أنشئ بيئة Python وثبّت المتطلبات:

```bash
pip install -r requirements.txt
```

2. عيّن التوكن كمتغير بيئة بدل وضعه داخل الكود:

```bash
export TELEGRAM_BOT_TOKEN="..."
```

3. شغّل البوت:

```bash
python telegram_bot.py
```

## الأمان

- لا تضع Telegram token أو `cookies.txt` أو ملفات `.env` في Git.
- استخدم `.env.example` كقالب فقط.
- أي token سبق نشره في Git يجب إلغاؤه واستبداله من BotFather لأن حذفه من الملف الحالي لا يمسحه من تاريخ Git.
