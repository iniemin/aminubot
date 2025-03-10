# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Modified by Vckyouuu @VckyouuBitch
# Using By Geez Project GPL-3.0 License

import io
import textwrap


from PIL import Image, ImageDraw, ImageFont

from pyAyiin import cmdHelp
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eod, eor

from . import cmd


@ayiinCmd(pattern="stick(.*)")
async def stext(event):
    sticktext = event.pattern_match.group(1)

    if not sticktext:
        return await eod(event, "`Mohon Maaf, Saya Membutuhkan Text Anda.`")
    await eor(event, "**Memproses...**")

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 200
    font = ImageFont.truetype(
        "assets/ProductSans-BoldItalic.ttf",
        size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(
            "assets/ProductSans-BoldItalic.ttf",
            size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2,
         (512 - height) / 2),
        sticktext,
        font=font,
        fill="white")

    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.client.send_file(event.chat_id, image_stream)


cmdHelp.update(
    {
        "stickerteks": f"**Plugin : **`stickerteks`\
        \n\n  »  **Perintah :** `{cmd}stick` `<teks>`\
        \n  »  **Kegunaan : **Membuat Sticker Text.\
    "
    }
)
