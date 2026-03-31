import random
from datetime import datetime
from pyrogram import filters
from pyrogram.enums import ChatType
from SANYAMUSIC import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import time

POLICE = [
    [
        InlineKeyboardButton(
            text="ᴏᴡɴᴇʀ",
            url="https://t.me/unrealaura",
        ),
    ],
]

# Stores last used time per chat
cooldown_dict = {}
COOLDOWN_SECONDS = 5 * 60  # 5 minutes


def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a


tomorrow = str(dt_tom())
today = str(dt()[0])


@app.on_message(filters.command("couples"))
async def ctest(_, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs.")

    # --- Cooldown Check ---
    chat_id = message.chat.id
    now = time.time()

    if chat_id in cooldown_dict:
        elapsed = now - cooldown_dict[chat_id]
        remaining = COOLDOWN_SECONDS - elapsed

        if remaining > 0:
            mins = int(remaining // 60)
            secs = int(remaining % 60)
            return await message.reply_text(
                f"**⏳ A Cᴏᴜᴘʟᴇ Hᴀꜱ Bᴇᴇɴ Dᴇᴄʟᴀʀᴇᴅ Rᴇᴄᴇɴᴛʟʏ.\n\⏰ Tʀʏ Aꜰᴛᴇʀ {mins}ᴍ {secs}s **"
            )

    # Update cooldown time
    cooldown_dict[chat_id] = now

    try:
        msg = await message.reply_text("ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴏᴜᴘʟᴇs...")

        list_of_users = []
        async for i in app.get_chat_members(message.chat.id, limit=50):
            if not i.user.is_bot:
                list_of_users.append(i.user.id)

        c1_id = random.choice(list_of_users)
        c2_id = random.choice(list_of_users)
        while c1_id == c2_id:
            c1_id = random.choice(list_of_users)

        N1 = (await app.get_users(c1_id)).mention
        N2 = (await app.get_users(c2_id)).mention

        TXT = f"""** ᴄᴜᴛɪᴇꜱ !! ᴏꜰ ᴛʜᴇ ᴅᴀʏ 💖 :

{N1} + {N2} = </𝟑

  **"""

        await msg.edit(TXT, reply_markup=InlineKeyboardMarkup(POLICE))

    except Exception as e:
        print(str(e))
        await msg.edit("**sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.**")
