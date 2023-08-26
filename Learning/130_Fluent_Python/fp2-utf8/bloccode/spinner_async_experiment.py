# Example 19-7. spinner_async_experiment.py: the supervisor and slow coroutines

async def slow() -> int:
    time.sleep(3)
    return 42

async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!'))
    print(f'spinner object: {spinner}')
    result = await slow()
    spinner.cancel()
    return result
