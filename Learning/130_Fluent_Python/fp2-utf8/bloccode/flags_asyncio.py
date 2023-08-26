# Example 21-3. flags_asyncio.py: imports and download functions

import asyncio

from httpx import AsyncClient

from flags import BASE_URL, save_flag, main

async def download_one(client: AsyncClient, cc: str):
    image = await get_flag(client, cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

async def get_flag(client: AsyncClient, cc: str) -> bytes:
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=6.1, follow_redirects=True)
    return resp.read()
