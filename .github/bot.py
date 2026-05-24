from telethon import TelegramClient
import asyncio
from telethon.sessions import StringSession
from telethon.tl.types import InputReplyToMessage
import os
import sys

API_ID = 611335
API_HASH = "d524b414d21f4d37f08684c1df41ac9c"

BETTER_NET = os.environ.get("BETTER_NET")
BBG = os.environ.get("BBG")
LXC = os.environ.get("LXC")
MOUNTIFY = os.environ.get("MOUNTIFY")
STOCK_CONFIG = os.environ.get("STOCK_CONFIG")
DROIDSPACES = os.environ.get("DROIDSPACES")
LTO = os.environ.get("LTO")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))
RUN_URL = os.environ.get("RUN_URL")
BOT_CI_SESSION = os.environ.get("BOT_CI_SESSION")
MSG_TEMPLATE = """
**New Build Published!**
*LTO: {lto}*
```Kernel Info
kernelver: {kernelversion}
stock: {stock}
BBG: {bbg}
Mountify support: {mountify}
lxc/docker support {lxc}
droidspaces: {droidspaces}
better net support: {better_net}
```
Please follow @esk_gki_build !
#GKI2 #ESK
[Workflow run]({run_url})
""".strip()


def get_caption():
    msg = MSG_TEMPLATE.format(
        lto=LTO,
        kernelversion=get_kernel_versions(),
        stock=STOCK_CONFIG,
        mountify=MOUNTIFY,
        lxc=LXC,
        droidspaces=DROIDSPACES,
        bbg=BBG,
        better_net=BETTER_NET,
        run_url=RUN_URL,
    )
    return msg


def get_kernel_versions():
    version = ""
    patchlevel = ""
    sublevel = ""

    try:
        with open("./kernel_workspace/common/Makefile", 'r') as file:
            for line in file:
                if line.startswith("VERSION"):
                    version = line.split('=')[1].strip()
                elif line.startswith("PATCHLEVEL"):
                    patchlevel = line.split('=')[1].strip()
                elif line.startswith("SUBLEVEL"):
                    sublevel = line.split('=')[1].strip()
                elif line.startswith("#"):  # skip comments
                    continue
                else:
                    break
    except FileNotFoundError:
        raise
    return f"{version}.{patchlevel}.{sublevel}"


async def send_telegram_message(file_path: str):
    async with TelegramClient(StringSession(BOT_CI_SESSION), api_id=API_ID, api_hash=API_HASH) as client:
        await client.start(bot_token=BOT_TOKEN)
        print("[+] Caption: ")
        print("---")
        print("---")
        print("[+] Sending")
        await client.send_file(
            entity=CHAT_ID,
            file=file_path,
            parse_mode="markdown",
            caption=get_caption(),
        )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)

    file_to_upload = sys.argv[1]
    if not os.path.isfile(file_to_upload):
        print(f"Error: {file_to_upload} does not exist!")
        sys.exit(1)

    asyncio.run(send_telegram_message(file_to_upload))
