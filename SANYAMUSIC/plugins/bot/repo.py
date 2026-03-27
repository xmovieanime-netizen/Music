import httpx
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SANYAMUSIC.utils.errors import capture_err 
from SANYAMUSIC import app
from config import BOT_USERNAME

# Caption Text
start_txt = """<b>❍ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ <u>ᴅɪᴠɪɴᴇ ᴄᴜʟᴛ ᴍᴜsɪᴄ 🎧</u></b>

:⧽ <b>ᴇᴀsʏ ᴅᴇᴘʟᴏʏ</b> –ᴏɴᴇ ᴄʟɪᴄᴋ ʜᴇʀᴏᴋᴜ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ  
:⧽ <b>ɴᴏ ʜᴇʀᴏᴋᴜ ᴏʀ ɪᴅ ʙᴀɴ ɪssᴜᴇs</b>  
:⧽ <b>ᴜɴʟɪᴍɪᴛᴇᴅ ᴅʏɴᴏs</b> – ʀᴜɴ 24/7 ʟᴀɢɢ-ғʀᴇᴇ """

# Repo Command Handler
@app.on_message(filters.command("repo"))
async def repo_handler(_, msg):
    buttons = [
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/divinecultgc"),
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/unrealaura"),
        ],
        [
            InlineKeyboardButton("ʀᴇᴘᴏ", callback_data="repo_contact")
            # InlineKeyboardButton("sᴀɴʏᴀ ᴍᴜsɪᴄ", url="https://github.com/urstark/sanyamusic/fork")
         ]
    ]

    await msg.reply_photo(
        photo="https://graph.org/file/6603c3740378d3f7187da.jpg",
        caption=start_txt,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

   
# --------------


@app.on_message(filters.command("repo", prefixes="#"))
@capture_err
async def repo(_, message):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/linux/contributors")
    
    if response.status_code == 200:
        users = response.json()
        list_of_users = ""
        count = 1
        for user in users:
            list_of_users += f"{count}. [{user['login']}]({user['html_url']})\n"
            count += 1

        text = f"""[𝖱𝖤𝖯𝖮 𝖫𝖨𝖭𝖪](https://github.com/linux) | [UPDATES](https://t.me/unrealaura)
| 𝖢𝖮𝖭𝖳𝖱𝖨𝖡𝖴𝖳𝖮𝖱𝖲 |
----------------
{list_of_users}"""
        await app.send_message(message.chat.id, text=text, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, text="Failed to fetch contributors.")



@app.on_callback_query(filters.regex("repo_contact"))
async def repo_contact_callback(client, query):
    await query.answer(
        "Repo is private. Contact Owner @unrealaura to get access.",
        show_alert=True
    )