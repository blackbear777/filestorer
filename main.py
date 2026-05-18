from pyrogram import Client, filters
import sqlite3
import random
import string

API_ID = 23075597
API_HASH = "b666a42d3e6ca6ce5942a04038bcaec0"
BOT_TOKEN = "8816697645:AAGw-k357a9s0N6MGMJom6IsZrxUympMUlY"

app = Client(
    "filestorebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# DATABASE
db = sqlite3.connect("files.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS files(
    code TEXT PRIMARY KEY,
    file_id TEXT,
    file_type TEXT,
    caption TEXT
)
""")
db.commit()

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# START COMMAND + LINK SUPPORT
@app.on_message(filters.command("start"))
async def start(client, message):

    if len(message.command) > 1:
        code = message.command[1]

        cursor.execute(
            "SELECT * FROM files WHERE code=?",
            (code,)
        )

        data = cursor.fetchone()

        if not data:
            return await message.reply_text("❌ File not found.")

        _, file_id, file_type, caption = data

        if file_type == "photo":
            await message.reply_photo(file_id, caption=caption)

        elif file_type == "video":
            await message.reply_video(file_id, caption=caption)

        elif file_type == "document":
            await message.reply_document(file_id, caption=caption)

    else:
        await message.reply_text(
            "📁 File Store Bot Ready!\n\n"
            "Send me photos, videos, or documents.\n"
            "I will generate a shareable link."
        )

# PHOTO SAVE
@app.on_message(filters.photo)
async def save_photo(client, message):

    file_id = message.photo.file_id
    caption = message.caption or ""
    code = generate_code()

    cursor.execute(
        "INSERT INTO files VALUES (?, ?, ?, ?)",
        (code, file_id, "photo", caption)
    )
    db.commit()

    bot_username = (await client.get_me()).username
    link = f"https://t.me/{bot_username}?start={code}"

    await message.reply_text(
        f"✅ Photo Saved!\n\n"
        f"🔗 Share Link:\n{link}\n\n"
        f"📦 Code: `{code}`"
    )

# VIDEO SAVE
@app.on_message(filters.video)
async def save_video(client, message):

    file_id = message.video.file_id
    caption = message.caption or ""
    code = generate_code()

    cursor.execute(
        "INSERT INTO files VALUES (?, ?, ?, ?)",
        (code, file_id, "video", caption)
    )
    db.commit()

    bot_username = (await client.get_me()).username
    link = f"https://t.me/{bot_username}?start={code}"

    await message.reply_text(
        f"✅ Video Saved!\n\n"
        f"🔗 Share Link:\n{link}\n\n"
        f"📦 Code: `{code}`"
    )

# DOCUMENT SAVE
@app.on_message(filters.document)
async def save_document(client, message):

    file_id = message.document.file_id
    caption = message.caption or ""
    code = generate_code()

    cursor.execute(
        "INSERT INTO files VALUES (?, ?, ?, ?)",
        (code, file_id, "document", caption)
    )
    db.commit()

    bot_username = (await client.get_me()).username
    link = f"https://t.me/{bot_username}?start={code}"

    await message.reply_text(
        f"✅ Document Saved!\n\n"
        f"🔗 Share Link:\n{link}\n\n"
        f"📦 Code: `{code}`"
    )

# MANUAL GET COMMAND
@app.on_message(filters.command("get"))
async def get_file(client, message):

    try:
        code = message.text.split(" ")[1]

        cursor.execute(
            "SELECT * FROM files WHERE code=?",
            (code,)
        )

        data = cursor.fetchone()

        if not data:
            return await message.reply_text("❌ File not found.")

        _, file_id, file_type, caption = data

        if file_type == "photo":
            await message.reply_photo(file_id, caption=caption)

        elif file_type == "video":
            await message.reply_video(file_id, caption=caption)

        elif file_type == "document":
            await message.reply_document(file_id, caption=caption)

    except:
        await message.reply_text("Usage:\n/get CODE")

# STATS
@app.on_message(filters.command("stats"))
async def stats(client, message):

    cursor.execute("SELECT COUNT(*) FROM files")
    total = cursor.fetchone()[0]

    await message.reply_text(
        f"📊 Total Saved Files: {total}"
    )

print("✅ Bot Started...")
app.run()
