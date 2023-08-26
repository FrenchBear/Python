result = []
async for i in aiter():
    if i % 2:
        result.append(i)
