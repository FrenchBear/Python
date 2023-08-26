# Example 21-15. tcp_mojifinder.py: search coroutine

async def search(query: str,
                 index: InvertedIndex,
                 writer: asyncio.StreamWriter) -> int:
    chars = index.search(query)
    lines = (line.encode() + CRLF for line
                in format_results(chars))
    writer.writelines(lines)
    await writer.drain()
    status_line = f'{"─" * 66} {len(chars)} found'
    writer.write(status_line.encode() + CRLF)
    await writer.drain()
    return len(chars)
