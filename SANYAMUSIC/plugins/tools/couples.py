import random
from datetime import datetime
from pyrogram import filters
from pyrogram.enums import ChatType
from SANYAMUSIC import app


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

        TXT = f"""**ᴀᴀᴊ ᴋᴀ ꜱᴀʙꜱᴇ ᴋᴀʟᴇꜱʜɪ ᴊᴏᴅᴀ 😊🔪 :

{N1} + {N2} = 💚

ᴀᴘɴᴀ ᴀᴜʀ ᴀᴘɴɪ ꜱᴇᴛᴛɪɴɢ ᴋᴀ ɴᴀᴀᴍ ꜱᴀᴛʜ ᴍᴀɪɴ ʟᴀᴀɴᴇ ᴋᴇ ʟɪʏᴇ [ᴅᴏᴏ ᴅᴀʙᴀʏᴇ](https://t.me/unrealaura) 🥀✨ !!**"""

        await msg.edit(TXT)

    except Exception as e:
        print(str(e))
        await msg.edit("**sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.**")
