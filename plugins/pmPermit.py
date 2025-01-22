# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Recode by @mrismanaziz
# @SharingUserbot
""" Userbot module for keeping control who PM you. """

from traceback import format_exc

from telethon import events
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.types import User

from pyAyiin import ayiin, cmdHelp
from pyAyiin.database.permit import (
    approve,
    delPermitMessage,
    disapprove,
    getPermitMessage,
    getModePermit,
    isApproved,
    setModePermit,
    setPermitMessage
)
from pyAyiin.database.variable import delVar, getVar, setVar
from pyAyiin.decorator import ayiinCmd, ayiinHandler
from pyAyiin.utils import eod, eor

from . import COUNT_PM, LASTMSG, cmd


DEF_UNAPPROVED_MSG =  (
    """
╔═════════════════════╗
│ ㅤ 𖣘𝚂𝙴𝙻𝙰𝙼𝙰𝚃 𝙳𝙰𝚃𝙰𝙽𝙶 𝚃𝙾𝙳𖣘ㅤ  ㅤ   
╚═════════════════════╝
⍟ 𝙹𝙰𝙽𝙶𝙰𝙽 𝚂𝙿𝙰𝙼 𝙲𝙷𝙰𝚃 𝙼𝙰𝙹𝙸𝙺𝙰𝙽 𝙶𝚄𝙰 𝙺𝙴𝙽𝚃𝙾𝙳
⍟ 𝙶𝚄𝙰 𝙰𝙺𝙰𝙽 𝙾𝚃𝙾𝙼𝙰𝚃𝙸𝚂 𝙱𝙻𝙾𝙺𝙸𝚁 𝙺𝙰𝙻𝙾 𝙻𝚄 𝚂𝙿𝙰𝙼
⍟ 𝙹𝙰𝙳𝙸 𝚃𝚄𝙽𝙶𝙶𝚄 𝚂𝙰𝙼𝙿𝙰𝙸 𝙼𝙰𝙹𝙸𝙺𝙰𝙽 𝙶𝚄𝙰 𝙽𝙴𝚁𝙸𝙼𝙰 𝙿𝙴𝚂𝙰𝙽 𝙻𝚄
╔═════════════════════╗
│ㅤㅤ𖣘 𝙿𝙴𝚂𝙰𝙽 𝙾𝚃𝙾𝙼𝙰𝚃𝙸𝚂 𖣘ㅤㅤ      
│ㅤㅤ𖣘 𝙰𝚈𝙸𝙸𝙽 - 𝚄𝚂𝙴𝚁𝙱𝙾𝚃 𖣘ㅤㅤ   
╚═════════════════════╝
"""
)


@ayiinHandler(incoming=True)
async def permitpm(event):
    """ Prohibits people from PMing you without approval. \
        Will block retarded nibbas automatically. """
    if not getModePermit():
        return
    self_user = await event.client.get_me()
    sender = await event.get_sender()
    if (
        event.is_private
        and event.chat_id != 777000
        and event.chat_id != self_user.id
        and not sender.bot
        and not sender.contact
    ):
        notifsoff = getVar("NOTIF_OFF")

        # This part basically is a sanity check
        # If the message that sent before is Unapproved Message
        # then stop sending it again to prevent FloodHit
        getmsg = getPermitMessage()
        UNAPPROVED_MSG = DEF_UNAPPROVED_MSG if not getmsg else getmsg
        apprv = isApproved()
        if event.chat_id not in apprv and event.text != UNAPPROVED_MSG:
            # Auto Approve Developer
            if event.chat_id in ayiin._devs:
                if event.chat_id not in apprv:
                    try:
                        approve(event.chat_id)
                        await event.client.send_message(ayiin.BOTLOG_CHATID, f"**#AUTO_APPROVED_DEVELOPER**\n\n👑 **Developer:** [{sender.first_name}](tg://user?id={sender.id})\n💬 `Developer Ayiin-Userbot Telah Mengirimi Anda Pesan...`")
                        await event.client.send_message(
                            event.chat_id,
                            f"**Menerima Pesan!!!**\n**Terdeteksi [{sender.first_name}](tg://user?id={sender.id}) Adalah Developer Ayiin-Userbot**"
                        )
                        return
                    except BaseException as e:
                        return await eor(event, "**KESALAHAN : **`{}`".format(e))
                else:
                    pass
            if event.chat_id in LASTMSG:
                prevmsg = LASTMSG[event.chat_id]
                # If the message doesn't same as previous one
                # Send the Unapproved Message again
                if event.text != prevmsg:
                    async for message in event.client.iter_messages(
                        event.chat_id, from_user="me", search=UNAPPROVED_MSG
                    ):
                        await message.delete()
                    await event.reply(f"{UNAPPROVED_MSG}")
            else:
                await event.reply(f"{UNAPPROVED_MSG}")
            LASTMSG.update({event.chat_id: event.text})
            if notifsoff:
                await event.client.send_read_acknowledge(event.chat_id)
            if event.chat_id not in COUNT_PM:
                COUNT_PM.update({event.chat_id: 1})
            else:
                COUNT_PM[event.chat_id] = COUNT_PM[event.chat_id] + 1

            if COUNT_PM[event.chat_id] > ayiin.PM_LIMIT:
                await event.respond(
                    "**Maaf Anda Diblokir karna melakukan spam ke tuan saya**"
                )

                try:
                    del COUNT_PM[event.chat_id]
                    del LASTMSG[event.chat_id]
                except KeyError:
                    if ayiin.BOTLOG_CHATID:
                        await event.client.send_message(
                            ayiin.BOTLOG_CHATID,
                            "**Terjadi Error Saat Menghitung Pesan pribadi, Mohon Restart Bot!**"
                        )
                    return ayiin.log.info("Gagal menghitung PM yang diterima")

                await event.client(BlockRequest(event.chat_id))
                await event.client(ReportSpamRequest(peer=event.chat_id))

                if ayiin.BOTLOG_CHATID:
                    name = await event.client.get_entity(event.chat_id)
                    name0 = str(name.first_name)
                    await event.client.send_message(
                        ayiin.BOTLOG_CHATID,
                        f"**[{name0}](tg://user?id={event.chat_id}) Telah diblokir karna melakukan spam ke tuan saya**"
                    )


@ayiinHandler(outgoing=True)
async def auto_accept(event):
    """Will approve automatically if you texted them first."""
    if not getModePermit():
        return
    self_user = await event.client.get_me()
    sender = await event.get_sender()
    if (
        event.is_private
        and event.chat_id != 777000
        and event.chat_id != self_user.id
        and not sender.bot
        and not sender.contact
    ):
        getmsg = getPermitMessage()
        UNAPPROVED_MSG = DEF_UNAPPROVED_MSG if not getmsg else getmsg
        chat = await event.get_chat()
        apprv = isApproved()
        if isinstance(chat, User):
            if event.chat_id in apprv or chat.bot:
                return
            async for message in event.client.iter_messages(
                event.chat_id, reverse=True, limit=1
            ):
                if (
                    message.text is not UNAPPROVED_MSG
                    and message.sender_id == self_user.id
                ):
                    approve(event.chat_id)

                if event.chat_id in apprv and ayiin.BOTLOG_CHATID:
                    await event.client.send_message(
                        ayiin.BOTLOG_CHATID,
                        "**#AUTO_APPROVED**\n"
                        + "👤 **User:** "
                        + f"[{chat.first_name}](tg://user?id={chat.id})",
                    )


@ayiinCmd(pattern="notifoff$")
async def notifoff(noff_event):
    """For .notifoff command, stop getting notifications from unapproved PMs."""
    setVar("NOTIF_OFF", True)
    await noff_event.edit(
        "**Notifikasi Pesan Pribadi Tidak Disetujui, Telah Dibisukan!**"
    )


@ayiinCmd(pattern="notifon$")
async def notifon(non_event):
    """For .notifoff command, get notifications from unapproved PMs."""
    delVar("NOTIF_OFF")
    await non_event.edit(
        "**Notifikasi Pesan Pribadi Disetujui, Tidak Lagi Dibisukan!**"
    )


@ayiinCmd(pattern="(?:setuju|ok)\\s?(.)?")
async def approvepm(apprvpm):
    """For .ok command, give someone the permissions to PM you."""
    apprv = isApproved()
    try:
        if apprvpm.reply_to_msg_id:
            reply = await apprvpm.get_reply_message()
            replied_user = await apprvpm.client.get_entity(reply.sender_id)
            uid = replied_user.id
            name0 = str(replied_user.first_name)

        elif apprvpm.pattern_match.group(1):
            inputArgs = apprvpm.pattern_match.group(1)

            try:
                inputArgs = int(inputArgs)
            except ValueError:
                pass

            try:
                user = await apprvpm.client.get_entity(inputArgs)
            except BaseException:
                return await eod(apprvpm, "**Invalid username/ID.**")

            if not isinstance(user, User):
                return await eod(
                    apprvpm,
                    "**Mohon Balas Pesan Pengguna Yang ingin diterima.**"
                )

            uid = user.id
            name0 = str(user.first_name)

        else:
            aname = await apprvpm.client.get_entity(apprvpm.chat_id)
            if not isinstance(aname, User):
                return await eod(
                    apprvpm,
                    "**Mohon Balas Pesan Pengguna Yang ingin diterima.**"
                )
            name0 = str(aname.first_name)
            uid = apprvpm.chat_id

        getmsg = getPermitMessage()
        UNAPPROVED_MSG = DEF_UNAPPROVED_MSG if not getmsg else getmsg
        async for message in apprvpm.client.iter_messages(
            apprvpm.chat_id, from_user="me", search=UNAPPROVED_MSG
        ):
            await message.delete()
        if uid in apprv:
            await eod(
                apprvpm,
                'Pengguna sudah ada di database',
                time=8
            )
            return
        else:
            approve(uid)
            await eod(
                apprvpm,
                f"**Menerima Pesan** [{name0}](tg://user?id={uid})",
                time=5
            )
    except BaseException:
        ayiin.log.error(format_exc())


@ayiinCmd(pattern="(?:tolak|nopm)\\s?(.)?")
async def disapprovepm(disapprvpm):
    apprv = isApproved()
    if disapprvpm.reply_to_msg_id:
        reply = await disapprvpm.get_reply_message()
        replied_user = await disapprvpm.client.get_entity(reply.sender_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        if aname not in apprv:
            await eod(
                disapprvpm,
                f" **Pengguna** [{name0}](tg://user?id={aname}) **Tidak ada di database**",
                time=8
            )
            return
        else:
            disapprove(aname)
            await eod(
                disapprvpm,
                f" **Maaf Ya** [{name0}](tg://user?id={aname}) **Pesan Anda Telah Ditolak, Mohon Untuk Tidak Melakukan Spam Ke Tuan Saya**",
                time=8
            )

    elif disapprvpm.pattern_match.group(1):
        inputArgs = disapprvpm.pattern_match.group(1)

        try:
            inputArgs = int(inputArgs)
        except ValueError:
            pass

        try:
            user = await disapprvpm.client.get_entity(inputArgs)
        except BaseException:
            return await eod(
                disapprvpm,
                "**Mohon Balas Pesan Pengguna Yang ingin ditolak.**"
            )

        if not isinstance(user, User):
            return await eod(
                disapprvpm,
                "**Mohon Balas Pesan Pengguna Yang ingin ditolak.**"
            )

        aname = user.id
        name0 = str(user.first_name)
        if aname not in apprv:
            await eod(
                disapprvpm,
                f"**Pengguna** [{name0}](tg://user?id={aname}) **Tidak ada di database**",
                time=8
            )
            return
        else:
            disapprove(aname)
            await eod(
                disapprvpm,
                f"**Maaf Ya** [{name0}](tg://user?id={aname}) **Pesan Anda Telah Ditolak, Mohon Untuk Tidak Melakukan Spam Ke Tuan Saya**",
                time=8
            )

    else:
        aname = await disapprvpm.client.get_entity(disapprvpm.chat_id)
        if not isinstance(aname, User):
            return await eod(
                disapprvpm,
                "**Ini hanya dapat dilakukan dengan pengguna.**"
            )
        name0 = str(aname.first_name)
        aname = aname.id
        if aname not in apprv:
            await eod(
                disapprvpm,
                f"**Pengguna** [{name0}](tg://user?id={aname}) **Tidak ada di database**",
                time=8
            )
            return
        else:
            disapprove(aname)
            await eod(
                disapprvpm,
                f"**Maaf Ya** [{name0}](tg://user?id={aname}) **Pesan Anda Telah Ditolak, Mohon Untuk Tidak Melakukan Spam Ke Tuan Saya**",
                time=8
            )


@ayiinCmd(pattern="block$")
async def blockpm(block):
    """For .block command, block people from PMing you!"""
    if block.reply_to_msg_id:
        reply = await block.get_reply_message()
        replied_user = await block.client.get_entity(reply.sender_id)
        aname = replied_user.id
        await block.client(BlockRequest(aname))
        await block.edit("**Maaf Anda telah Diblokir oleh Tuan Saya!**")
        uid = replied_user.id
    else:
        await block.client(BlockRequest(block.chat_id))
        aname = await block.client.get_entity(block.chat_id)
        if not isinstance(aname, User):
            return await block.edit("**Ini hanya dapat dilakukan dengan pengguna.**")
        await block.edit("**Maaf Anda telah Diblokir oleh Tuan Saya!**")
        uid = block.chat_id

    disapprove(uid)

@ayiinCmd(pattern="unblock$")
async def unblockpm(unblock):
    """For .unblock command, let people PMing you again!"""
    if unblock.reply_to_msg_id:
        reply = await unblock.get_reply_message()
        replied_user = await unblock.client.get_entity(reply.sender_id)
        await unblock.client(UnblockRequest(replied_user.id))
        await unblock.edit("**Anda Telah Bebas Dari Blokir Karna Tuan Saya Lagi Baik.**")


@ayiinCmd(pattern="permit (on|off)(?: |$)(\\w*)")
async def Setting_permit_mode(cust_msg):
    conf = cust_msg.pattern_match.group(1)
    if conf.lower() == "on":
        setModePermit(mode=True)
        await cust_msg.client.send_message(
            cust_msg.chat_id,
            "PM PERMIT Anda Berhasil Diaktifkan."
        )

    if conf.lower() == "off":
        setModePermit(mode=None)
        await cust_msg.client.send_message(
            cust_msg.chat_id,
            "PM PERMIT Anda Berhasil Dimatikan."
        )


@ayiinCmd(pattern="(set|get|reset) pmpermit(?: |$)(\\w*)")
async def add_pmsg(cust_msg):
    """Set your own Unapproved message"""
    if not getModePermit():
        return await cust_msg.edit(
            f"**Anda Harus Mengaktifkan PM_PERMIT Terlebih dahulu**\n\n**Bila ingin Mengaktifkan PMPERMIT Silahkan Ketik:** `{cmd}permit on`"
        )
    await cust_msg.edit('**Memproses...**')
    conf = cust_msg.pattern_match.group(1)

    custom_message = getPermitMessage()

    if conf.lower() == "set":
        message = await cust_msg.get_reply_message()
        status = "Pesan"

        # check and clear user unapproved message first
        if custom_message is not None:
            delPermitMessage()
            status = "Pesan"

        if not message:
            return await cust_msg.edit("**Mohon Balas Kepesan...**")

        # TODO: allow user to have a custom text formatting
        # eg: bold, underline, striketrough, link
        # for now all text are in monoscape
        msg = message.message  # get the plain text
        setPermitMessage(msg)
        await cust_msg.edit("**Pesan Berhasil Disimpan Ke Room Chat**")

        if ayiin.BOTLOG_CHATID:
            await cust_msg.client.send_message(
                ayiin.BOTLOG_CHATID,
                f"**Pesan PMPERMIT Yang Tersimpan:** \n\n{msg}"
            )

    if conf.lower() == "reset":
        if custom_message is None:
            await cust_msg.edit(
                "`Anda Telah Menghapus Pesan Custom PMPERMIT menjadi Default`"
            )

        else:
            delPermitMessage()
            await cust_msg.edit(
                "`Pesan PMPERMIT Anda Sudah Default Sejak Awal`"
            )
    if conf.lower() == "get":
        if custom_message is not None:
            await cust_msg.edit(
                f"**Pesan PMPERMIT Yang Sekarang:**\n\n{custom_message}"
            )
        else:
            await cust_msg.edit(
                f"**Anda Belum Menyetel Pesan Costum PMPERMIT,**\n**Masih Menggunakan Pesan PMPERMIT Default:**\n\n{DEF_UNAPPROVED_MSG}"
            )



cmdHelp.update(
    {
        "pmpermit": f"**Plugin : **`pmpermit`\
        \n\n  »  **Perintah :** `{cmd}setuju` atau `{cmd}ok`\
        \n  »  **Kegunaan : **Menerima pesan seseorang dengan cara balas pesannya atau tag dan juga untuk dilakukan di pm.\
        \n\n  »  **Perintah :** `{cmd}tolak` atau `{cmd}nopm`\
        \n  »  **Kegunaan : **Menolak pesan seseorang dengan cara balas pesannya atau tag dan juga untuk dilakukan di pm.\
        \n\n  »  **Perintah :** `{cmd}block`\
        \n  »  **Kegunaan : **Memblokir Orang Di PM.\
        \n\n  »  **Perintah :** `{cmd}unblock`\
        \n  »  **Kegunaan : **Membuka Blokir.\
        \n\n  »  **Perintah :** `{cmd}notifoff`\
        \n  »  **Kegunaan : **Menghidupkan notifikasi pesan yang belum diterima.\
        \n\n  »  **Perintah :** `{cmd}notifon`\
        \n  »  **Kegunaan : **Menghidupkan notifikasi pesan yang belum diterima.\
        \n\n  »  **Perintah :** `{cmd}set pmpermit` <balas ke pesan>\
        \n  »  **Kegunaan : **Menyetel Pesan Pribadimu untuk orang yang pesannya belum diterima.\
        \n\n  »  **Perintah :** `{cmd}get pmpermit`\
        \n  »  **Kegunaan : **Mendapatkan Custom pesan PM mu.\
        \n\n  »  **Perintah :** `{cmd}reset pmpermit`\
        \n  »  **Kegunaan : **Menghapus pesan PM ke default.\
        \n\n  •  **Pesan Pribadi yang belum diterima saat ini tidak dapat disetel ke teks format kaya bold, underline, link, dll. Pesan akan terkirim normal saja**\
        \n\n**NOTE: Bila ingin Mengaktifkan PMPERMIT Silahkan Ketik:** `{cmd}permit on`\
    "
    }
)
