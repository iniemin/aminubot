# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#
# Kalo mau ngecopas, jangan hapus credit ya goblok

import asyncio

from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from pyAyiin import ayiin, cmdHelp
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eod, eor

from . import cmd


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call, limit=1))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i: i + n]


@ayiinCmd(pattern="startvc$")
async def start_voice(c):
    me = await c.client.get_me()
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await eod(c, f"**Maaf {me.first_name} Bukan Admin 👮**")
        return
    try:
        await c.client(startvc(c.chat_id))
        await eor(c, "`Voice Chat Started...`")
    except Exception as ex:
        await eod(c, f"**ERROR:** `{ex}`")


@ayiinCmd(pattern="stopvc$")
async def stop_voice(c):
    me = await c.client.get_me()
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await eod(c, f"**Maaf {me.first_name} Bukan Admin 👮**")
        return
    try:
        await c.client(stopvc(await get_call(c)))
        await eor(c, "`Voice Chat Stopped...`")
    except Exception as ex:
        await eod(c, f"**ERROR:** `{ex}`")


@ayiinCmd(pattern="vcinvite")
async def vc_invite(c):
    xxnx = await eor(c, "`Inviting Members to Voice Chat...`")
    users = []
    z = 0
    async for x in c.client.iter_participants(c.chat_id):
        if not x.bot:
            users.append(x.id)
    botyins = list(user_list(users, 6))
    for p in botyins:
        try:
            await c.client(invitetovc(call=await get_call(c), users=p))
            z += 6
        except BaseException:
            pass
    await xxnx.edit(f"`{z}` **Orang Berhasil diundang ke VCG**")


@ayiinCmd(pattern="vctitle(?: |$)(.*)")
async def change_title(e):
    title = e.pattern_match.group(1)
    me = await e.client.get_me()
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not title:
        return await eod(e, "**Silahkan Masukan Title Obrolan Suara Grup**")

    if not admin and not creator:
        await eod(e, f"**Maaf {me.first_name} Bukan Admin 👮**")
        return
    try:
        await e.client(settitle(call=await get_call(e), title=title.strip()))
        await eor(e, f"**Berhasil Mengubah Judul VCG Menjadi** `{title}`")
    except Exception as ex:
        await eod(e, f"**ERROR:** `{ex}`")


@ayiinCmd(pattern="joinvc(?: |$)(.*)", only="groups")
async def join_vc(a):
    xx = await eor(a, "****ᴍᴇᴍᴘʀᴏꜱᴇꜱ...**")
    if len(a.text.split()) > 1:
        chat_id = a.text.split()[1]
        try:
            chat_id = await a.client.get_peer_id(int(chat_id))
        except Exception as e:
            return await xx.edit(f'ERROR: {e}')
    else:
        chat_id = a.chat_id
    try:
        await ayiin.tgCalls.play(chat_id)
        await ayiin.tgCalls.mute_stream(chat_id)
        await xx.edit(
            f"⍟ [{ayiin.me.first_name}](tg://user?id={ayiin.me.id})\n\n❏ **ʙᴇʀʜᴀꜱɪʟ ʙᴇʀɢᴀʙᴜɴɢ ᴋᴇ ᴏʙʀᴏʟᴀɴ ꜱᴜᴀʀᴀ**\n└ **ᴄʜᴀᴛ ɪᴅ:** `{chat_id}`"
        )
    except Exception as e:
        await xx.edit(f'ERROR: {e}')


@ayiinCmd(pattern="leavevc(?: |$)(.*)", only="groups")
async def leave_vc(event):
    xx = await eor(event, "**Memproses...**")
    if len(event.text.split()) > 1:
        chat_id = event.text.split()[1]
        try:
            chat_id = await event.client.get_peer_id(int(chat_id))
        except Exception as e:
            return await xx.edit(f'ERROR: {e}')
    else:
        chat_id = event.chat_id
    try:
        await ayiin.tgCalls.leave_call(chat_id)
        await xx.edit(
            f"⍟ [{ayiin.me.first_name}](tg://user?id={ayiin.me.id})\n\n❏ **Berhasil Meninggalkan Obrolan Suara**\n└ **Chat ID:** `{event.chat_id}`"
        )
        return
    except Exception as e:
        return await xx.edit(f'ERROR: {e}')



cmdHelp.update(
    {
        "vctools": f"**Plugin : **`vctools`\
        \n\n  •  **Syntax :** `{cmd}startvc`\
        \n  •  **Function : **Untuk Memulai voice chat group\
        \n\n  •  **Syntax :** `{cmd}stopvc`\
        \n  •  **Function : **Untuk Memberhentikan voice chat group\
        \n\n  •  **Syntax :** `{cmd}vctitle` <title vcg>\
        \n  •  **Function : **Untuk Mengubah title/judul voice chat group\
        \n\n  •  **Syntax :** `{cmd}vcinvite`\
        \n  •  **Function : **Mengundang Member group ke voice chat group\
        \n\n  •  **Syntax :** `{cmd}joinvc`\
        \n  •  **Function : **Untuk bergabung ke obrolan suara menggunakan bot anda\
        \n\n  •  **Syntax :** `{cmd}leavevc`\
        \n  •  **Function : **Untuk meninggalkan obrolan suara\
    "
    }
)
