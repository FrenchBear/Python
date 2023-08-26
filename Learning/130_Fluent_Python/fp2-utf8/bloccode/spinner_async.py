# Example 19-9. spinner_async.py: the asynchronous supervisor coroutine

async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!'))
    print('spinner object:', spinner)
    result = await slow()
    spinner.cancel()
    return result
