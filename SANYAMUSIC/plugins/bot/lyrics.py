import random
import re
import string

import aiohttp
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from SANYAMUSIC import app
from SANYAMUSIC.utils.decorators.language import language
from config import BANNED_USERS, lyrical


async def fetch_lyrics(title: str) -> dict:
    """Fetch lyrics using free lyrics.ovh API"""
    # Try splitting into artist + song
    parts = title.split("-", 1) if "-" in title else title.split(" ", 1)
    if len(parts) == 2:
        artist, song = parts[0].strip(), parts[1].strip()
    else:
        artist, song = "", title.strip()

    urls = []
    if artist and song:
        urls.append(f"https://api.lyrics.ovh/v1/{artist}/{song}")
    urls.append(f"https://api.lyrics.ovh/v1/{title}/")

    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        lyrics = data.get("lyrics")
                        if lyrics:
                            return {"lyrics": lyrics.strip(), "found": True}
            except Exception:
                continue

    # Fallback: try searching via lrclib.net (completely free, no key)
    try:
        async with aiohttp.ClientSession() as session:
            params = {"q": title}
            async with session.get(
                "https://lrclib.net/api/search",
                params=params,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and len(data) > 0:
                        plain = data[0].get("plainLyrics")
                        if plain:
                            return {"lyrics": plain.strip(), "found": True}
    except Exception:
        pass

    return {"lyrics": None, "found": False}


@app.on_message(filters.command(["lyrics"]) & ~BANNED_USERS)
@language
async def lrsearch(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(_["lyrics_1"])

    title = message.text.split(None, 1)[1]
    m = await message.reply_text(_["lyrics_2"])

    result = await fetch_lyrics(title)

    if not result["found"] or not result["lyrics"]:
        return await m.edit(_["lyrics_3"].format(title))

    ran_hash = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    lyrical[ran_hash] = result["lyrics"]

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["L_B_1"],
                    url=f"https://t.me/{app.username}?start=lyrics_{ran_hash}",
                ),
            ]
        ]
    )

    await m.edit(_["lyrics_4"], reply_markup=upl)