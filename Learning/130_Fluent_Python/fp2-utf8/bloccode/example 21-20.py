# Example 21-20. Example using @asynccontextmanager and loop.run_in_executor

from contextlib import asynccontextmanager

@asynccontextmanager
async def web_page(url):
    loop = asyncio.get_running_loop()
    data = await loop.run_in_executor(
        None, download_webpage, url)
    yield data
    await loop.run_in_executor(None, update_stats, url)

async with web_page('google.com') as data:
    process(data)
