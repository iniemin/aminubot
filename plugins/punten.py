from time import sleep

from pyAyiin import cmdHelp
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eor

from . import cmd


@ayiinCmd(pattern="sadboy(?: |$)(.*)")
async def _(event):
    xx = await eor(event, "`Pertama-tama kamu cantik`")
    sleep(2)
    await xx.edit("`Kedua kamu manis`")
    sleep(1)
    await xx.edit("`Dan yang terakhir adalah kamu bukan jodohku`")


# Create by myself @localheart


@ayiinCmd(pattern="punten(?: |$)(.*)")
async def _(event):
    text = """
`┻┳|―-∩`
`┳┻|     ヽ`
`┻┳|    ● |`
`┳┻|▼) _ノ`
`┻┳|￣  )`
`┳ﾐ(￣ ／`
`┻┳T￣|`

**Punten**"""
    await eor(
        event,
        text
    )


@ayiinCmd(pattern="pantau(?: |$)(.*)")
async def _(event):
    await eor(
        event,
        "`\n┻┳|―-∩`"
        "`\n┳┻|     ヽ`"
        "`\n┻┳|    ● |`"
        "`\n┳┻|▼) _ノ`"
        "`\n┻┳|￣  )`"
        "`\n┳ﾐ(￣ ／`"
        "`\n┻┳T￣|`"
        "\n**Masih Gua Pantau**"
    )


# Create by myself @localheart


cmdHelp.update(
    {
        "punten": f"**Plugin : **`Animasi Punten`\
        \n\n  »  **Perintah :** `{cmd}punten` ; `{cmd}pantau`\
        \n  »  **Kegunaan : **Arts Beruang kek lagi mantau.\
        \n\n  »  **Perintah :** `{cmd}sadboy`\
        \n  »  **Kegunaan : **ya sadboy coba aja.\
    "
    }
)
