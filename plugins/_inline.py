import random
import re

from telethon import Button
from telethon.sync import custom, events
from telethon.tl.types import InputWebDocument

from pyAyiin import ayiin, cmdHelp


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
                ayiin.INLINE_PIC,
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
                ayiin.INLINE_PIC,
                0,
                "image/jpeg",
                []),
            text=f"**Ayiin-Userbot**\n➖➖➖➖➖➖➖➖➖➖\n✧ **ᴏᴡɴᴇʀ :** [{ayiin.me.first_name}](tg://user?id={ayiin.me.id})\n✧ **ᴀssɪsᴛᴀɴᴛ:** {ayiin.bot.me.username}\n➖➖➖➖➖➖➖➖➖➖\n**ᴜᴘᴅᴀᴛᴇs :** @AyiinChannel\n➖➖➖➖➖➖➖➖➖➖",
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
