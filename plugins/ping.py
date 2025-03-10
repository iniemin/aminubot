# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# ReCode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de


import time
from datetime import datetime

from time import sleep
from speedtest import Speedtest


from pyAyiin import cmdHelp, startTime
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eod, eor

from . import cmd


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@ayiinCmd("ping$")
async def pingCommand(ping):
    uptime = await get_readable_time((time.time() - startTime))
    start = datetime.now()
    Ayiin = await eor(ping, "**✧**")
    await Ayiin.edit("**✧✧**")
    await Ayiin.edit("**✧✧✧**")
    await Ayiin.edit("**✧✧✧✧**")
    await Ayiin.edit("**✧✧✧✧✧**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    user = await ping.client.get_me()
    await Ayiin.edit("⚡")
    sleep(3)
    await Ayiin.edit(
        f"""
**✧ ᴀʏɪɪɴ-ᴜsᴇʀʙᴏᴛ ✧**

✧ **ᴘɪɴɢ :** `{duration}ms`
✧ **ᴜᴘᴛɪᴍᴇ :** `{uptime}`
✧ **ᴏᴡɴᴇʀ :** [{user.first_name}](tg://user?id={user.id})
"""
    )


@ayiinCmd(pattern="xping$", only="groups")
async def xpingCommand(ping):
    uptime = await get_readable_time((time.time() - startTime))
    start = datetime.now()
    xping = await eor(ping, "`Pinging....`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await xping.edit(
        f"**PONG!! 🍭**\n**Pinger** : %sms\n**Bot Uptime** : {uptime}🕛" % (duration)
    )


@ayiinCmd(pattern="lping$")
async def lpingCommand(ping):
    uptime = await get_readable_time((time.time() - startTime))
    start = datetime.now()
    lping = await eor(ping, "**★ PING ★**")
    await lping.edit("**★★ PING ★★**")
    await lping.edit("**★★★ PING ★★★**")
    await lping.edit("**★★★★ PING ★★★★**")
    await lping.edit("**✦҈͜͡➳ PONG!**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    user = await ping.client.get_me()
    await lping.edit(
        f"❃ **Ping !!** "
        f"`%sms` \n"
        f"❃ **Uptime -** "
        f"`{uptime}` \n"
        f"**✦҈͜͡➳ Master :** [{user.first_name}](tg://user?id={user.id})" % (duration)
    )


@ayiinCmd(pattern="keping$")
async def kepingCommand(pong):
    await get_readable_time((time.time() - startTime))
    start = datetime.now()
    kopong = await eor(pong, "**『⍟𝐊𝐎𝐍𝐓𝐎𝐋』**")
    await kopong.edit("**◆◈𝐊𝐀𝐌𝐏𝐀𝐍𝐆◈◆**")
    await kopong.edit("**𝐏𝐄𝐂𝐀𝐇𝐊𝐀𝐍 𝐁𝐈𝐉𝐈 𝐊𝐀𝐔 𝐀𝐒𝐔**")
    await kopong.edit("**☬𝐒𝐈𝐀𝐏 𝐊𝐀𝐌𝐏𝐀𝐍𝐆 𝐌𝐄𝐍𝐔𝐌𝐁𝐔𝐊 𝐀𝐒𝐔☬**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    user = await pong.client.get_me()
    await kopong.edit(
        f"**✲ 𝙺𝙾𝙽𝚃𝙾𝙻 𝙼𝙴𝙻𝙴𝙳𝚄𝙶** "
        f"\n ⫸ 𝙺𝙾𝙽𝚃𝙾𝙻 `%sms` \n"
        f"**✲ 𝙱𝙸𝙹𝙸 𝙿𝙴𝙻𝙴𝚁** "
        f"\n ⫸ 𝙺𝙰𝙼𝙿𝙰𝙽𝙶『[{user.first_name}](tg://user?id={user.id})』 \n" % (duration)
    )


# .keping & kping Coded by Koala


@ayiinCmd(pattern=r"kping$")
async def kpingCommand(pong):
    uptime = await get_readable_time((time.time() - startTime))
    start = datetime.now()
    kping = await eor(pong, "8✊===D")
    await kping.edit("8=✊==D")
    await kping.edit("8==✊=D")
    await kping.edit("8===✊D")
    await kping.edit("8==✊=D")
    await kping.edit("8=✊==D")
    await kping.edit("8✊===D")
    await kping.edit("8=✊==D")
    await kping.edit("8==✊=D")
    await kping.edit("8===✊D")
    await kping.edit("8==✊=D")
    await kping.edit("8=✊==D")
    await kping.edit("8✊===D")
    await kping.edit("8=✊==D")
    await kping.edit("8==✊=D")
    await kping.edit("8===✊D")
    await kping.edit("8===✊D💦")
    await kping.edit("8====D💦💦")
    await kping.edit("**CROOTTTT**")
    await kping.edit("**CROOTTTT AAAHHH.....**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await kping.edit("🥵")
    sleep(3)
    await kping.edit(
        f"**𝙽𝙶𝙴𝙽𝚃𝙾𝚃 𝙰𝙷𝙷!! 🥵**\n**𝙺𝚄𝚃𝙰𝙽𝙶** : %sms\n**𝙱𝙾𝚃 𝚄𝙿𝚃𝙸𝙼𝙴** : {uptime}🕛" % (duration)
    )


@ayiinCmd(pattern="pong$")
async def pongCommand(pong):
    start = datetime.now()
    xx = await eor(pong, "`Sepong`")
    await xx.edit("Sepong Sayang.....")
    end = datetime.now()
    duration = (end - start).microseconds / 9000
    await xx.edit("🥵")
    sleep(3)
    await xx.edit("**𝙿𝙸𝙽𝙶!**\n`%sms`" % (duration))


cmdHelp.update(
    {
        "ping": f"**Plugin : **`ping`\
        \n\n  »  **Perintah :** `{cmd}ping` ; `{cmd}lping` ; `{cmd}xping` ; `{cmd}kping`\
        \n  »  **Kegunaan : **Untuk menunjukkan ping userbot.\
        \n\n  »  **Perintah :** `{cmd}pong`\
        \n  »  **Kegunaan : **Sama seperti perintah ping\
    "
    }
)


cmdHelp.update(
    {
        "speedtest": f"**Plugin : **`speedtest`\
        \n\n  »  **Perintah :** `{cmd}speedtest`\
        \n  »  **Kegunaan : **Untuk Mengetes kecepatan server userbot.\
    "
    }
)
