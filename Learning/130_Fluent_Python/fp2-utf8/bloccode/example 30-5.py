# Example 30-5. Shorten string by clipping at space near the desired length.

def clip(text, max_len=80):
    """Return max_len characters clipped at space if possible"""
    text = text.rstrip()
    if len(text) <= max_len or ' ' not in text:
        return text
    end = len(text)
    space_at = text.rfind(' ', 0, max_len + 1)
    if space_at >= 0:
        end = space_at
    else:
        space_at = text.find(' ', max_len)
        if space_at >= 0:
            end = space_at
    return text[:end].rstrip()
