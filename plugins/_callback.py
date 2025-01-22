import random
import re

from telethon import Button
from telethon.sync import custom, events
from telethon.tl.types import InputWebDocument

from pyAyiin import ayiin, cmdHelp
from pyAyiin.database.handler import getHandler
from pyAyiin.database.sudo import getSudo



BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")


main_help_button = [
    [
        Button.inline("•• Pʟᴜɢɪɴ ••", data="reopen"),
        Button.inline("Mᴇɴᴜ Vᴄ ••", data="inline_yins"),
    ],
    [
        Button.inline("⚙️ Aʟᴀᴛ Pᴇᴍɪʟɪᴋ", data="yins_langs"),
        Button.url("Pᴇɴɢᴀᴛᴜʀᴀɴ ⚙️", url=f"t.me/{ayiin.bot.me.username}?start="),
    ],
    [Button.inline("•• Kᴇᴍʙᴀʟɪ ••", data="close")],
]


@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"reopen")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    logoyins = random.choice(
        [
            "assets/inline1.png",
            "assets/inline2.png",
            "assets/inline3.png"
        ]
    )
    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        buttons = ayiin.paginateHelp(0, cmdHelp, "helpme")
        text = f"**✨ ᴀʏɪɪɴ-ᴜsᴇʀʙᴏᴛ ɪɴʟɪɴᴇ ᴍᴇɴᴜ ✨**\n\n⍟ **ᴅᴇᴘʟᴏʏ :** •[{ayiin._host}]•\n⍟ **ᴏᴡɴᴇʀ** {ayiin.me.first_name}\n⍟ **ᴊᴜᴍʟᴀʜ :** {len(cmdHelp)} **Modules**"
        await event.edit(
            text,
            file=logoyins,
            buttons=buttons,
            link_preview=False,
        )
    else:
        reply_pop_up_alert = f"Kamu Tidak diizinkan, ini Userbot Milik {ayiin.me.first_name}"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


@ayiin.bot.on(events.InlineQuery)
async def inline_handler(event):
    builder = event.builder
    result = None
    query = event.text
    logoyins = random.choice(
        [
            "assets/inline1.png",
            "assets/inline2.png",
            "assets/inline3.png"
        ]
    )
    botusername = ayiin.bot.me.username
    if event.query.user_id == ayiin.me.id and query.startswith(
            "@AyiinChats"):
        buttons = ayiin.paginateHelp(0, cmdHelp, "helpme")
        result = await event.builder.photo(
            file=logoyins,
            link_preview=False,
            text=f"**✨ ᴀʏɪɪɴ-ᴜsᴇʀʙᴏᴛ ɪɴʟɪɴᴇ ᴍᴇɴᴜ ✨**\n\n⍟ **ᴅᴇᴘʟᴏʏ :** •[{ayiin._host}]•\n⍟ **ᴏᴡɴᴇʀ :** {ayiin.me.first_name}\n⍟ **ᴊᴜᴍʟᴀʜ :** {len(cmdHelp)} **Modules**",
            buttons=main_help_button,
        )
    elif query.startswith("repo"):
        result = builder.article(
            title="Repository",
            description="Repository Ayiin - Userbot",
            url="https://t.me/AyiinChats",
            thumb=InputWebDocument(
                logoyins,
                0,
                "image/jpeg",
                []),
            text="**Ayiin-Userbot**\n➖➖➖➖➖➖➖➖➖➖\n✧  **ʀᴇᴘᴏ :** [AyiinXd](https://t.me/AyiinXd)\n✧ **sᴜᴘᴘᴏʀᴛ :** @AyiinChats\n✧ **ʀᴇᴘᴏsɪᴛᴏʀʏ :** [Ayiin-Userbot](https://github.com/AyiinXd/Ayiin-Userbot)\n➖➖➖➖➖➖➖➖➖➖",
            buttons=[
                [
                    custom.Button.url(
                        "ɢʀᴏᴜᴘ",
                        "https://t.me/AyiinChats"),
                    custom.Button.url(
                        "ʀᴇᴘᴏ",
                        "https://github.com/AyiinXd/Ayiin-Userbot"),
                ],
            ],
            link_preview=False,
        )
    elif query.startswith("Inline buttons"):
        markdown_note = query[14:]
        prev = 0
        note_data = ""
        buttons = []
        for match in BTN_URL_REGEX.finditer(markdown_note):
            n_escapes = 0
            to_check = match.start(1) - 1
            while to_check > 0 and markdown_note[to_check] == "\\":
                n_escapes += 1
                to_check -= 1
            if n_escapes % 2 == 0:
                buttons.append(
                    (match.group(2), match.group(3), bool(
                        match.group(4))))
                note_data += markdown_note[prev: match.start(1)]
                prev = match.end(1)
            elif n_escapes % 2 == 1:
                note_data += markdown_note[prev:to_check]
                prev = match.start(1) - 1
            else:
                break
        else:
            note_data += markdown_note[prev:]
        message_text = note_data.strip()
        tl_ib_buttons = ayiin.buildKeyboard(buttons)
        result = builder.article(
            title="Inline creator",
            text=message_text,
            buttons=tl_ib_buttons,
            link_preview=False,
        )
    else:
        result = builder.article(
            title="✨ ᴀʏɪɪɴ-ᴜsᴇʀʙᴏᴛ ✨",
            description="Ayiin - Userbot | Telethon",
            url="https://t.me/AyiinChannel",
            thumb=InputWebDocument(
                logoyins,
                0,
                "image/jpeg",
                []),
            text=f"**Ayiin-Userbot**\n➖➖➖➖➖➖➖➖➖➖\n✧ **ᴏᴡɴᴇʀ :** [{ayiin.me.first_name}](tg://user?id={ayiin.me.id})\n✧ **ᴀssɪsᴛᴀɴᴛ:** {botusername}\n➖➖➖➖➖➖➖➖➖➖\n**ᴜᴘᴅᴀᴛᴇs :** @AyiinChannel\n➖➖➖➖➖➖➖➖➖➖",
            buttons=[
                [
                    custom.Button.url(
                        "ɢʀᴏᴜᴘ",
                        "https://t.me/AyiinChats"),
                    custom.Button.url(
                        "ʀᴇᴘᴏ",
                        "https://github.com/AyiinXd/Ayiin-Userbot"),
                ],
            ],
            link_preview=False,
        )
    await event.answer(
        [result], switch_pm="👥 USERBOT PORTAL", switch_pm_param="start"
    )

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(
        data=re.compile(rb"helpme_next\((.+?)\)")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()

    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        current_page_number = int(
            event.data_match.group(1).decode("UTF-8"))
        buttons = ayiin.paginateHelp(
            current_page_number + 1, cmdHelp, "helpme")
        await event.edit(buttons=buttons)
    else:
        reply_pop_up_alert = (
            f"Kamu Tidak diizinkan, ini Userbot Milik {ayiin.me.first_name}"
        )
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"helpme_close\((.+?)\)")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    logoyins = random.choice(
        [
            "assets/inline1.png",
            "assets/inline2.png",
            "assets/inline3.png"
        ]
    )
    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:  # @Kyy-Userbot
        # https://t.me/TelethonChat/115200
        await event.edit(
            file=logoyins,
            link_preview=True,
            buttons=main_help_button)

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"gcback")
    )
)
async def gback_handler(event):
    sudoer = getSudo()
    logoyins = random.choice(
        [
            "assets/inline1.png",
            "assets/inline2.png",
            "assets/inline3.png"
        ]
    )
    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:  # @Ayiin-Userbot
        # https://t.me/TelethonChat/115200
        text = (
            f"**✨ ᴀʏɪɪɴ-ᴜsᴇʀʙᴏᴛ ɪɴʟɪɴᴇ ᴍᴇɴᴜ ✨**\n\n✧ **ᴏᴡɴᴇʀ :** [{ayiin.me.first_name}](tg://user?id={ayiin.me.id})\n✧ **ᴊᴜᴍʟᴀʜ :** {len(cmdHelp)} **Modules**")
        await event.edit(
            text,
            file=logoyins,
            link_preview=True,
            buttons=main_help_button)


@ayiin.bot.on(events.CallbackQuery(data=b"inline_yins"))
async def about(event):
    sudoer = getSudo()

    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        await event.edit(f"""
•Menu• - Voice chat group untuk [{ayiin.me.first_name}](tg://user?id={ayiin.me.id})
""",
                            buttons=[
                                [
                                    Button.inline("⍟ ᴠᴄ ᴘʟᴜɢɪɴ ⍟",
                                                data="vcplugin"),
                                    Button.inline("⍟ ᴠᴄ ᴛᴏᴏʟs ⍟",
                                                data="vctools")],
                                [custom.Button.inline(
                                    "ʙᴀᴄᴋ", data="gcback")],
                            ]
                            )
    else:
        reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nAnda Tidak Mempunyai Hak Untuk Menekan Tombol Button Ini"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"vcplugin")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    cmd = getHandler()

    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        text = (
            f"""
✘ **Perintah yang tersedia di vcplugin** ✘

»  **Perintah : **`{cmd}play` <Judul Lagu/Link YT>
»  **Kegunaan :** __Untuk Memutar Lagu di voice chat group dengan akun kamu.__

»  **Perintah : **`{cmd}vplay` <Judul Video/Link YT>
»  **Kegunaan :** __Untuk Memutar Video di voice chat group dengan akun kamu.__

»  **Perintah : **`{cmd}end`
»  **Kegunaan :** __Untuk Memberhentikan video/lagu yang sedang putar di voice chat group.__

»  **Perintah : **`{cmd}skip`
»  **Kegunaan :** __Untuk Melewati video/lagu yang sedang di putar.__

»  **Perintah : **`{cmd}pause`
»  **Kegunaan :** __Untuk memberhentikan video/lagu yang sedang diputar.__

»  **Perintah : **`{cmd}resume`
»  **Kegunaan :** __Untuk melanjutkan pemutaran video/lagu yang sedang diputar.__

»  **Perintah : **`{cmd}volume` 1-200
»  **Kegunaan :** __Untuk mengubah volume (Membutuhkan Hak admin).__

»  **Perintah : **`{cmd}playlist`
»  **Kegunaan :** __Untuk menampilkan daftar putar Lagu/Video.__
""")
        logoyins = random.choice(
            [
                "assets/inline1.png",
                "assets/inline2.png",
                "assets/inline3.png"
            ]
        )
        await event.edit(
            text,
            file=logoyins,
            link_preview=True,
            buttons=[Button.inline("ʙᴀᴄᴋ", data="inline_yins")])
    else:
        reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nAnda Tidak Mempunyai Hak Untuk Menekan Tombol Button Ini"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"vctools")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    cmd = getHandler()
    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        text = (
            f"""
✘ **Perintah yang tersedia di vctools** ✘

»  **Perintah : **`{cmd}startvc`
»  **Kegunaan :** __Untuk Memulai voice chat group.__

»  **Perintah : **`{cmd}stopvc`
»  **Kegunaan :** __Untuk Memberhentikan voice chat group.__

»  **Perintah :** `{cmd}joinvc`
»  **Kegunaan :** __Untuk Bergabung ke voice chat group.__

»  **Perintah : **`{cmd}leavevc`
»  **Kegunaan :** __Untuk Turun dari voice chat group.__

»  **Perintah : **`{cmd}vctitle` <title vcg>
»  **Kegunaan :** __Untuk Mengubah title/judul voice chat group.__

»  **Perintah : **`{cmd}vcinvite`
»  **Kegunaan :** __Mengundang Member group ke voice chat group.__
""")
        logoyins = random.choice(
            [
                "assets/inline1.png",
                "assets/inline2.png",
                "assets/inline3.png"
            ]
        )
        await event.edit(
            text,
            file=logoyins,
            link_preview=True,
            buttons=[Button.inline("ʙᴀᴄᴋ", data="inline_yins")])
    else:
        reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nAnda Tidak Mempunyai Hak Untuk Menekan Tombol Button Ini"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"yins_langs")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    cmd = getHandler()

    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        text = (
            f"""
✘ **Perintah yang tersedia di tools** ✘

»  **Perintah :** `{cmd}lang`
»  **Kegunaan : **Untuk Mengubah Bahasa.

»  **Perintah :** `{cmd}string`
»  **Kegunaan : **Untuk Membuat String Session.
""")
        logoyins = random.choice(
            [
                "assets/inline1.png",
                "assets/inline2.png",
                "assets/inline3.png"
            ]
        )
        await event.edit(
            text,
            file=logoyins,
            link_preview=True,
            buttons=[Button.inline("ʙᴀᴄᴋ", data="gcback")])
    else:
        reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nAnda Tidak Mempunyai Hak Untuk Menekan Tombol Button Ini"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@ayiin.bot.on(events.CallbackQuery(data=b"close"))
async def close(event):
    buttons = [
        (custom.Button.inline("ᴍᴀɪɴ ᴍᴇɴᴜ", data="gcback"),),
    ]
    logoyins = random.choice(
        [
            "assets/inline1.png",
            "assets/inline2.png",
            "assets/inline3.png"
        ]
    )
    await event.edit("**ᴍᴇɴᴜ ᴅɪᴛᴜᴛᴜᴘ**", file=logoyins, buttons=buttons)

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(
        data=re.compile(rb"helpme_prev\((.+?)\)")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()

    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        current_page_number = int(
            event.data_match.group(1).decode("UTF-8"))
        buttons = ayiin.paginateHelp(
            current_page_number - 1, cmdHelp, "helpme")
        await event.edit(buttons=buttons)
    else:
        reply_pop_up_alert = f"Kamu Tidak diizinkan, ini Userbot Milik {ayiin.me.first_name}"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@ayiin.bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ub_modul_(.*)")))
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    cmd = getHandler()
    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        modul_name = event.data_match.group(1).decode("UTF-8")

        cmdhel = str(cmdHelp[modul_name])
        if len(cmdhel) > 950:
            help_string = (
                str(cmdHelp[modul_name])
                .replace("`", "")
                .replace("**", "")[:950]
                + "..."
                + f"\n\nBaca Teks Berikutnya Ketik {cmd}help "
                + modul_name
                + " "
            )
        else:
            help_string = (str(cmdHelp[modul_name]).replace(
                "`", "").replace("**", ""))

        reply_pop_up_alert = (
            help_string
            if help_string is not None
            else "{} Tidak ada dokumen yang telah ditulis untuk modul.".format(
                modul_name
            )
        )
        await event.edit(
            reply_pop_up_alert, buttons=[
                Button.inline("ʙᴀᴄᴋ", data="reopen")]
        )

    else:
        reply_pop_up_alert = f"Kamu Tidak diizinkan, ini Userbot Milik {ayiin.me.first_name}"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
