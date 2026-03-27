import time, re, asyncio
from config import BOT_USERNAME
from pyrogram.enums import MessageEntityType
from pyrogram import filters
from pyrogram.types import Message
from SANYAMUSIC import app
from SANYAMUSIC.mongo.readable_time import get_readable_time
from SANYAMUSIC.mongo.afkdb import add_afk, is_afk, remove_afk

# Helper function to delete AFK messages after 30 seconds
async def auto_delete_afk(msg, delay=30):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except:
        pass

@app.on_message(filters.command(["afk", "brb"], prefixes=["/", "!"]))
async def active_afk(_, message: Message):
    if message.sender_chat:
        return
    user_id = message.from_user.id
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            
            # Only text replies
            if afktype == "text":
                send = await message.reply_text(
                    f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    disable_web_page_preview=True,
                )
            elif afktype == "text_reason":
                send = await message.reply_text(
                    f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`",
                    disable_web_page_preview=True,
                )
            else:
                # For animation, photo, or sticker - only send text
                send = await message.reply_text(
                    f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`" if reasonafk and str(reasonafk) != "None" else f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    disable_web_page_preview=True,
                )
            asyncio.create_task(auto_delete_afk(send))
        except Exception:
            send = await message.reply_text(
                f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ",
                disable_web_page_preview=True,
            )
            asyncio.create_task(auto_delete_afk(send))

    if len(message.command) == 1 and not message.reply_to_message:
        details = {"type": "text", "time": time.time(), "data": None, "reason": None}
    elif len(message.command) > 1 and not message.reply_to_message:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {"type": "text_reason", "time": time.time(), "data": None, "reason": _reason}
    elif len(message.command) == 1 and message.reply_to_message.animation:
        # Store as text instead of animation
        details = {"type": "text", "time": time.time(), "data": None, "reason": None}
    elif len(message.command) > 1 and message.reply_to_message.animation:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {"type": "text_reason", "time": time.time(), "data": None, "reason": _reason}
    elif len(message.command) == 1 and message.reply_to_message.photo:
        # Store as text instead of photo
        details = {"type": "text", "time": time.time(), "data": None, "reason": None}
    elif len(message.command) > 1 and message.reply_to_message.photo:
        _reason = message.text.split(None, 1)[1].strip()
        details = {"type": "text_reason", "time": time.time(), "data": None, "reason": _reason}
    elif len(message.command) == 1 and message.reply_to_message.sticker:
        # Store as text instead of media
        details = {"type": "text", "time": time.time(), "data": None, "reason": None}
    elif len(message.command) > 1 and message.reply_to_message.sticker:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {"type": "text_reason", "time": time.time(), "data": None, "reason": _reason}
    else:
        details = {"type": "text", "time": time.time(), "data": None, "reason": None}

    await add_afk(user_id, details)    
    send = await message.reply_text(f"**{message.from_user.first_name}** ɪs ɴᴏᴡ ᴀғᴋ!")
    asyncio.create_task(auto_delete_afk(send))

chat_watcher_group = 1

@app.on_message(~filters.me & ~filters.bot & ~filters.via_bot, group=chat_watcher_group)
async def chat_watcher_func(_, message):
    if message.sender_chat:
        return
    userid = message.from_user.id
    user_name = message.from_user.first_name

    # Fixed: Prevent the watcher from waking you up if the current message is the AFK command
    if message.text or message.caption:
        msg_check = message.text or message.caption
        if msg_check.startswith(("/", "!")):
            parts = msg_check.split()
            if parts and parts[0][1:].lower() in ["afk", "brb", "ye"]:
                return

    msg = ""
    replied_user_id = 0
    
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            
            if afktype == "text":
                msg += f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n"
            elif afktype == "text_reason":
                msg += f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n"
        except:
            msg += f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ\n\n"

    if message.reply_to_message:
        try:
            replied_first_name = message.reply_to_message.from_user.first_name
            replied_user_id = message.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time((int(time.time() - timeafk)))
                    
                    if afktype == "text":
                        msg += f"**{replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"
                    elif afktype == "text_reason":
                        msg += f"**{replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n"
                except Exception:
                    msg += f"**{replied_first_name}** ɪs ᴀғᴋ\n\n"
        except:
            pass

    if message.entities:
        entity = message.entities
        j = 0
        for x in range(len(entity)):
            if (entity[j].type) == MessageEntityType.MENTION:
                found = re.findall("@([_0-9a-zA-Z]+)", message.text)
                try:
                    get_user = found[j]
                    user = await app.get_users(get_user)
                    if user.id == replied_user_id:
                        j += 1
                        continue
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time((int(time.time() - timeafk)))
                        
                        if afktype == "text":
                            msg += f"**{user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"
                        elif afktype == "text_reason":
                            msg += f"**{user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n"
                    except:
                        msg += f"**{user.first_name[:25]}** ɪs ᴀғᴋ\n\n"
            elif (entity[j].type) == MessageEntityType.TEXT_MENTION:
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = entity[j].user.first_name
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time((int(time.time() - timeafk)))
                        
                        if afktype == "text":
                            msg += f"**{first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"
                        elif afktype == "text_reason":
                            msg += f"**{first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\nʀᴇᴀsᴏɴ: `{reasonafk}`\n\n"
                    except:
                        msg += f"**{first_name[:25]}** ɪs ᴀғᴋ\n\n"
            j += 1
    if msg != "":
        try:
            send = await message.reply_text(msg, disable_web_page_preview=True)
            asyncio.create_task(auto_delete_afk(send))
        except:
            return