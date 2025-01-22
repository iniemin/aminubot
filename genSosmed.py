import asyncio
from sosmed import Sosmed

sosmed = Sosmed()


async def mainSosmed():
    res = await sosmed.auth(prompt=True)
    print(f"\nYour SOSMED_API_KEY: {res.token}")
    print(f"Your SOSMED_SECRET: {res.secret}\n")


asyncio.run(mainSosmed())
