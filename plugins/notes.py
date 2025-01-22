# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands for keeping notes. """

from asyncio import sleep
from traceback import format_exc

from pyAyiin import ayiin, cmdHelp
from pyAyiin.decorator import ayiinCmd
from pyAyiin.database.notes import addNote, getNote, getNotes, rmNote, updateNote

from . import cmd


def check_for_notes(chat_id, trigger):
    all_notes = getNotes(chat_id)
    for keywords in all_notes:
        keyword = keywords[1]
        if trigger == keyword:
            return True
    return False


@ayiinCmd(pattern="notes$")
async def notes_active(svd):
    message = "**Catatan yang disimpan dalam obrolan ini:**\n"
    notes = getNotes(svd.chat_id)
    if notes:
        for note in notes:
            message += f"`- {note[1]}`\n"
        msg = message + "\n\nGunakan #notename Untuk mendapatkan catatan"
        await svd.edit(message)
    else:
        await svd.edit("**Tidak ada catatan yang disimpan dalam obrolan ini**")


@ayiinCmd(pattern="clear (\\w*)")
async def remove_notes(clr):
    """For .clear command, clear note with the given name."""
    notename = clr.pattern_match.group(1)
    cek = check_for_notes(clr.chat_id, notename)
    if not cek:
        return await clr.edit(
            f"**Tidak dapat menemukan catatan:** `{notename}`"
        )
    else:
        rmNote(clr.chat_id, notename)
        return await clr.edit(f"**Berhasil Menghapus Catatan:** `{notename}`")


@ayiinCmd(pattern="save (\\w*)")
async def save_note(fltr):
    keyword = fltr.pattern_match.group(1)
    string = fltr.text.partition(keyword)[2]
    msg = await fltr.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if ayiin.BOTLOG_CHATID:
            await fltr.client.send_message(
                ayiin.BOTLOG_CHATID,
                f"#NOTE\nCHAT ID: {fltr.chat_id}\nKEYWORD: {keyword}\n\nPesan berikut disimpan sebagai data balasan catatan untuk obrolan, mohon JANGAN dihapus !!"
            )
            msg_o = await fltr.client.forward_messages(
                entity=ayiin.BOTLOG_CHATID, messages=msg, from_peer=fltr.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            return await fltr.edit(
                "**Menyimpan media sebagai data untuk catatan memerlukan BOTLOG_CHATID untuk disetel.**"
            )
    elif fltr.reply_to_msg_id and not string:
        rep_msg = await fltr.get_reply_message()
        string = rep_msg.text
    cek = check_for_notes(fltr.chat_id, keyword)
    if not cek:
        addNote(str(fltr.chat_id), keyword, string, msg_id)
        return await fltr.edit(f"**Catatan Berhasil disimpan. Gunakan** `#{keyword}` **untuk mengambilnya**")
    else:
        updateNote(str(fltr.chat_id), keyword, string, msg_id)
        return await fltr.edit(f"**Catatan Berhasil diperbarui. Gunakan** `#{keyword}` **untuk mengambilnya**")


@ayiinCmd(
    pattern=r"#\w*",
    disableEdited=True,
    disableErrors=True,
)
async def incom_note(getnt):
    """Notes logic."""
    notename = getnt.text[1:]
    note = getNote(getnt.chat_id, notename)
    message_id_to_reply = getnt.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if note:
        if note[3]:
            msg_o = await getnt.client.get_messages(
                entity=ayiin.BOTLOG_CHATID, ids=int(note[3])
            )
            await getnt.client.send_message(
                getnt.chat_id,
                msg_o.mesage,
                reply_to=message_id_to_reply,
                file=msg_o.media,
            )
        elif note[2]:
            await getnt.client.send_message(
                getnt.chat_id, note[2], reply_to=message_id_to_reply
            )


@ayiinCmd(pattern="rmbotnotes (.*)")
async def kick_marie_notes(kick):
    """ For .rmbotnotes command, allows you to kick all \
        Marie(or her clones) notes from a chat. """
    bot_type = kick.pattern_match.group(1).lower()
    if bot_type not in ["marie", "rose"]:
        return await kick.edit("`Bot itu belum didukung!`")
    await kick.edit("`Akan menghapus semua Catatan!`")
    await sleep(3)
    resp = await kick.get_reply_message()
    filters = resp.text.split("-")[1:]
    for i in filters:
        if bot_type == "marie":
            await kick.reply("/clear %s" % (i.strip()))
        if bot_type == "rose":
            i = i.replace("`", "")
            await kick.reply("/clear %s" % (i.strip()))
        await sleep(0.3)
    await kick.respond("`Berhasil membersihkan catatan bot yaay!`\n Beri aku cookie!")
    if ayiin.BOTLOG_CHATID:
        await kick.client.send_message(
            ayiin.BOTLOG_CHATID,
            f"Saya membersihkan semua Catatan di {kick.chat_id}"
        )


cmdHelp.update(
    {
        "notes": f"**Plugin : **`Notes`\
        \n\n  »  **Perintah :** `#<notename>`\
        \n  »  **Kegunaan : **Mendapat catatan yang ditentukan.\
        \n\n  »  **Perintah :** `{cmd}save` <notename> <notedata> atau balas pesan dengan .save <notename>\
        \n  »  **Kegunaan : **Menyimpan pesan yang dibalas sebagai catatan dengan notename. (Bekerja dengan foto, dokumen, dan stiker juga!).\
        \n\n  »  **Perintah :** `{cmd}notes`\
        \n  »  **Kegunaan : **Mendapat semua catatan yang disimpan dalam obrolan \
        \n\n  »  **Perintah :** `{cmd}clear` <notename>\
        \n  »  **Kegunaan : **Menghapus catatan yang ditentukan. \
        \n\n  »  **Perintah :** `{cmd}rmbotnotes` <marie / rose>\
        \n  »  **Kegunaan : **Menghapus semua catatan bot admin (Saat ini didukung: Marie, Rose, dan klonnya.) Dalam obrolan.\
    "
    }
)
