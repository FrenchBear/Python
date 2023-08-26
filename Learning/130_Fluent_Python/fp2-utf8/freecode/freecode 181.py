async with semaphore:
    image = await get_flag(client, base_url, cc)
