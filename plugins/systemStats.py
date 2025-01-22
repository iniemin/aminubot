# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for System Stats commands """

import asyncio
import platform
import sys
import time
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from datetime import datetime
from os import remove
from shutil import which

import psutil
from pytgcalls import __version__ as pyTgCallsVersion

from pyAyiin import ayiin, cmdHelp, startTime
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eor
from pyAyiin.lib.tools import bash

from . import cmd
from .ping import get_readable_time

try:
    from carbonnow import Carbon
except ImportError:
    Carbon = None

modules = cmdHelp
emoji = ayiin.ALIVE_EMOJI
alive_text = ayiin.ALIVE_TEKS_CUSTOM


@ayiinCmd(
    pattern="sysinfo$",
)
async def _(e):
    xxnx = await eor(e, "`Processing...`")
    x, y = await bash("neofetch|sed 's/\x1B\\[[0-9;\\?]*[a-zA-Z]//g' >> neo.txt")
    with open("neo.txt", "r") as neo:
        p = (neo.read()).replace("\n\n", "")
    ok = Carbon(base_url="https://carbonara.vercel.app/api/cook", code=p)
    haa = await ok.memorize("neofetch")
    await e.reply(file=haa)
    await xxnx.delete()
    remove("neo.txt")


@ayiinCmd(pattern=r"spc")
async def psu(event):
    uname = platform.uname()
    softw = "**Iɴғᴏʀᴍᴀsɪ Sɪsᴛᴇᴍ**\n"
    softw += f"**Sɪsᴛᴇᴍ   :** `{uname.system}`\n"
    softw += f"**Rɪʟɪs    :** `{uname.release}`\n"
    softw += f"**Vᴇʀsɪ    :** `{uname.version}`\n"
    softw += f"**Mᴇsɪɴ    :** `{uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"**Wᴀᴋᴛᴜ Hɪᴅᴜᴘ:** `{bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**Iɴғᴏʀᴍᴀsɪ CPU**\n"
    cpuu += "**Pʜʏsɪᴄᴀʟ Cᴏʀᴇs   :** `" + \
        str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "**Tᴏᴛᴀʟ Cᴏʀᴇs      :** `" + \
        str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"**Mᴀx Fʀᴇǫᴜᴇɴᴄʏ    :** `{cpufreq.max:.2f}Mhz`\n"
    cpuu += f"**Mɪɴ Fʀᴇǫᴜᴇɴᴄʏ    :** `{cpufreq.min:.2f}Mhz`\n"
    cpuu += f"**Cᴜʀʀᴇɴᴛ Fʀᴇǫᴜᴇɴᴄʏ:** `{cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**CPU Usᴀɢᴇ Pᴇʀ Cᴏʀᴇ**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"**Cᴏʀᴇ {i}  :** `{percentage}%`\n"
    cpuu += "**Tᴏᴛᴀʟ CPU Usᴀɢᴇ**\n"
    cpuu += f"**Sᴇᴍᴜᴀ Cᴏʀᴇ:** `{psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**Mᴇᴍᴏʀʏ Dɪɢᴜɴᴀᴋᴀɴ**\n"
    memm += f"**Tᴏᴛᴀʟ     :** `{get_size(svmem.total)}`\n"
    memm += f"**Aᴠᴀɪʟᴀʙʟᴇ :** `{get_size(svmem.available)}`\n"
    memm += f"**Usᴇᴅ      :** `{get_size(svmem.used)}`\n"
    memm += f"**Pᴇʀᴄᴇɴᴛᴀɢᴇ:** `{svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "**Bᴀɴᴅᴡɪᴛʜ Dɪɢᴜɴᴀᴋᴀɴ**\n"
    bw += f"**Uɴɢɢᴀʜ  :** `{get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"**Dᴏᴡɴʟᴏᴀᴅ:** `{get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{softw}\n"
    help_string += f"{cpuu}\n"
    help_string += f"{memm}\n"
    help_string += f"{bw}\n"
    help_string += "**Iɴғᴏʀᴍᴀsɪ Mᴇsɪɴ**\n"
    help_string += f"**Pʏᴛʜᴏɴ :** `{sys.version}`\n"
    help_string += f"**Tᴇʟᴇᴛʜᴏɴ :**`{ayiin._telethonVersion}`\n"
    help_string += f"**Pʏ-Aʏɪɪɴ :** `{ayiin._baseVersion}`\n"
    help_string += f"**Aʏɪɪɴ-Vᴇʀsɪᴏɴ :** `{ayiin.BOT_VER} [{ayiin._host}]`"
    await eor(event, help_string)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@ayiinCmd(pattern="sysd$")
async def sysdetails(sysd):
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + \
                str(stderr.decode().strip())

            await eor(sysd, "`" + result + "`")
        except FileNotFoundError:
            await eor(sysd, "**Install neofetch Terlebih dahulu!!**")


@ayiinCmd(pattern="botver$")
async def bot_ver(event):
    if event.text[0].isalpha() or event.text[0] in ("/", "#", "@", "!"):
        return
    if which("git") is not None:
        ver = await asyncrunapp(
            "git",
            "describe",
            "--all",
            "--long",
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        rev = await asyncrunapp(
            "git",
            "rev-list",
            "--all",
            "--count",
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        await eor(
            event,
            "✧ **Userbot Versi :** " f"`{verout}`" "\n✧ **Revisi :** " f"`{revout}`",
        )
    else:
        await eor(
            event, "anda tidak memiliki git, Anda Menjalankan Bot - 'v1.beta.4'!"
        )


@ayiinCmd(pattern="(?:alive|yinson)\\s?(.)?")
async def amireallyalive(alive):
    user = await alive.client.get_me()
    uptime = await get_readable_time((time.time() - startTime))
    await alive.edit("😈")
    await asyncio.sleep(3)
    output = (
        f"**Tʜᴇ [Aʏɪɪɴ-Usᴇʀʙᴏᴛ](https://github.com/AyiinXd/Ayiin-Userbot)**\n\n"
        f"**{alive_text}**\n\n"
        f"╭✠╼━━━━━━━━━━━━━━━✠╮\n"
        f"{emoji} **Aʏɪɪɴ Vᴇʀsɪᴏɴ :** `{ayiin.BOT_VER}`\n"
        f"{emoji} **Bᴏᴛ Uᴘᴛɪᴍᴇ :** `{uptime}`\n"
        f"{emoji} **Dᴇᴘʟᴏʏ Oɴ :** {ayiin._host}\n"
        f"{emoji} **Mᴏᴅᴜʟᴇs :** `{len(modules)} Modules` \n"
        f"{emoji} **Oᴡɴᴇʀ :** [{user.first_name}](tg://user?id={user.id}) \n"
        f"{emoji} **Pʏᴛʜᴏɴ Vᴇʀsɪᴏɴ :** `{ayiin._pythonVersion}` \n"
        f"{emoji} **PʏTɢCᴀʟʟs Vᴇʀsɪᴏɴ :** `{pyTgCallsVersion}` \n"
        f"{emoji} **Pʏ-Aʏɪɪɴ Vᴇʀsɪᴏɴ :** `{ayiin._baseVersion}`\n"
        f"{emoji} **Tᴇʟᴇᴛʜᴏɴ Vᴇʀsɪᴏɴ :** `{ayiin._telethonVersion}` \n"
        "╰✠╼━━━━━━━━━━━━━━━✠╯\n\n"
    )
    if ayiin.ALIVE_LOGO:
        try:
            logo = ayiin.ALIVE_LOGO
            await alive.delete()
            await alive.client.send_file(alive.chat_id, logo, caption=output)
        except BaseException:
            await alive.edit(
                output
            )
            return
    else:
        await eor(alive, output)


cmdHelp.update(
    {
        "system": f"**Plugin : **`system`.\
        \n\n  »  **Perintah :** `{cmd}sysinfo`\
        \n  »  **Kegunaan : **Informasi sistem menggunakan neofetch mengirim sebagai gambar.\
        \n\n  »  **Perintah :** `{cmd}sysd`\
        \n  »  **Kegunaan : **Informasi sistem menggunakan neofetch.\
        \n\n\n  »  **Perintah :** `{cmd}botver`\
        \n  »  **Kegunaan : **Menampilkan versi userbot.\
        \n\n  »  **Perintah :** `{cmd}spc`\
        \n  »  **Kegunaan : **Menampilkan spesifikasi sistem secara lengkap.\
    "
    }
)


cmdHelp.update(
    {
        "alive": f"**Plugin : **`alive`\
        \n\n  »  **Perintah :** `{cmd}alive` atau `{cmd}yinson`\
        \n  »  **Kegunaan : **Untuk melihat apakah bot Anda berfungsi atau tidak.\
    "
    }
)
