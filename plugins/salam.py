from time import sleep

from pyAyiin import cmdHelp
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eor

from . import cmd


@ayiinCmd(pattern="p(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**Assalamualaikum Dulu Biar Sopan**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@ayiinCmd(pattern="pe(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id,
        "**Assalamualaikum Warahmatullahi Wabarakatuh**",
        reply_to=event.reply_to_msg_id,
    )
    await event.delete()


@ayiinCmd(pattern="P(?: |$)(.*)")
async def _(event):
    me = await event.client.get_me()
    xx = await eor(event, f"**Haii Salken Saya {me.first_name}**")
    sleep(2)
    await xx.edit("**Assalamualaikum...**")


@ayiinCmd(pattern="l(?: |$)(.*)")
async def _(event):
    await event.client.send_message(
        event.chat_id, "**Wa'alaikumsalam**", reply_to=event.reply_to_msg_id
    )
    await event.delete()


@ayiinCmd(pattern="a(?: |$)(.*)")
async def _(event):
    me = await event.client.get_me()
    xx = await eor(event, f"**Haii Salken Saya {me.first_name}**")
    sleep(2)
    await xx.edit("**Assalamualaikum**")


@ayiinCmd(pattern="j(?: |$)(.*)")
async def _(event):
    xx = await eor(event, "**JAKA SEMBUNG BAWA GOLOK**")
    sleep(3)
    await xx.edit("**NIMBRUNG GOBLOKK!!!🔥**")


@ayiinCmd(pattern="k(?: |$)(.*)")
async def _(event):
    me = await event.client.get_me()
    xx = await eor(event, f"**Hallo KIMAAKK SAYA {me.first_name}**")
    sleep(2)
    await xx.edit("**LU SEMUA NGENTOT 🔥**")


@ayiinCmd(pattern="ass(?: |$)(.*)")
async def _(event):
    xx = await eor(event, "**Salam Dulu Biar Sopan**")
    sleep(2)
    await xx.edit("**السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ**")


cmdHelp.update(
    {
        "salam": f"**Plugin : **`salam`\
        \n\n  »  **Perintah :** `{cmd}p`\
        \n  »  **Kegunaan : **Assalamualaikum Dulu Biar Sopan..\
        \n\n  »  **Perintah :** `{cmd}pe`\
        \n  »  **Kegunaan : **salam Kenal dan salam\
        \n\n  »  **Perintah :** `{cmd}l`\
        \n  »  **Kegunaan : **Untuk Menjawab salam\
        \n\n  »  **Perintah :** `{cmd}ass`\
        \n  »  **Kegunaan : **Salam Bahas arab\
        \n\n  »  **Perintah :** `{cmd}semangat`\
        \n  »  **Kegunaan : **Memberikan Semangat.\
        \n\n  »  **Perintah :** `{cmd}ywc`\
        \n  »  **Kegunaan : **Menampilkan Sama sama\
        \n\n  »  **Perintah :** `{cmd}sayang`\
        \n  »  **Kegunaan : **Kata I Love You.\
        \n\n  »  **Perintah :** `{cmd}k`\
        \n  »  **Kegunaan : **LU SEMUA NGENTOT 🔥\
        \n\n  »  **Perintah :** `{cmd}j`\
        \n  »  **Kegunaan : **NIMBRUNG GOBLOKK!!!🔥\
    "
    }
)
