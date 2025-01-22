# Port by Koala 🐨/@manuskarakitann
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot/>
# t.me/SharingUserbot & t.me/Lunatic0de
# Nyenyenye bacot

from sosmed import Sosmed
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from pyAyiin import cmdHelp
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eod, eor

from . import cmd, var


sosmed = Sosmed(
    apiToken=var.SOSMED_API_KEY,
    secret=var.SOSMED_SECRET,
)


@ayiinCmd(pattern="dez(?: |$)(.*)")
async def DeezLoader(event):
    if event.fwd_from:
        return
    dlink = event.pattern_match.group(1)
    if ".com" not in dlink:
        await eod(
            event,
            "`Mohon Berikan Link Deezloader yang ingin di download`"
        )
    else:
        await eor(event, "`Mengunduh...`")
    chat = "@DeezLoadBot"
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message(dlink)
            details = await conv.get_response()
            song = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message(dlink)
            details = await conv.get_response()
            song = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(event.chat_id, song, caption=details.text)
        await event.delete()


@ayiinCmd(pattern="(fb|ig|tt|tw)(?: |$)(.*)")
async def sosmedDownloader(event):
    provider = event.pattern_match.group(1)
    link = event.pattern_match.group(2)
    if not link:
        return await eod(event, "**Mohon Berikan Link**", time=10)
    xx = await eor(event, "`Mengunduh...`")
    try:
        if provider == "fb":
            resFb = await sosmed.facebook(link)
            file = await resFb.download()
            await event.client.send_file(event.chat_id, file)
        elif provider == "ig":
            resIg = await sosmed.instagram(link)
            file = await resIg.download()
            await event.client.send_file(event.chat_id, file)
        elif provider == "tt":
            resTt = await sosmed.tiktok(link)
            file = await resTt.download()
            await event.client.send_file(event.chat_id, file)
        elif provider == "tw":
            resTw = await sosmed.twitter(link)
            file = await resTw.download()
            await event.client.send_file(event.chat_id, file)
    except Exception as e:
        return await eod(xx, str(e))
    await xx.delete()


cmdHelp.update(
    {
        "sosmed": f"**Plugin : **`sosmed`\
        \n\n  »  **Perintah :** `{cmd}dez` <link>\
        \n  »  **Kegunaan : **Download Lagu Via Deezloader\
        \n\n  »  **Perintah :** `{cmd}fb` <link>\
        \n  »  **Kegunaan : **Facebook Downloader Video.\
        \n\n  »  **Perintah :** `{cmd}ig` <link>\
        \n  »  **Kegunaan : **Instagram Downloader Video.\
        \n\n  »  **Perintah :** `{cmd}tt` <link>\
        \n  »  **Kegunaan : **Tiktok Downloader Video.\
        \n\n  »  **Perintah :** `{cmd}tw` <link>\
        \n  »  **Kegunaan : **Twitter Downloader Video.\
    "
    }
)


cmdHelp.update(
    {
        "tiktok": f"**Plugin : **`tiktok`\
        \n\n  »  **Perintah :** `{cmd}tiktok` <link>\
        \n  »  **Kegunaan : **Download Video Tiktok Tanpa Watermark\
    "
    }
)
