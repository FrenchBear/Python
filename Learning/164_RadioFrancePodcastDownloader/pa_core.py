# pa_core.py - Core processing of Radio France podcasts
#
# 2025-10-20    PV      First version (archives download)
# 2025-10-21    PV      Version for podcast downloader
# 2025-11-02    PV      Better replacement of " in sanitize_filename
# 2025-11-04    PV      sanitize_filename replace non-breaking space by regular space
# 2025-12-29    PV      Errors and wanings in color to be more visible

from datetime import datetime
import os
import re
import json
import requests


def print_ansi(code: str, *args):
    print(f'\033[{code}m', end='')
    print(*args, end='')
    print('\033[0m')

def print_error(*args):
    print_ansi('31;1', *args)   # red, bright

def print_warning(*args):
    print_ansi('33', *args)     # yellow


def memoize_web_page(f):
    memory = {}

    def inner(s):
        if s not in memory:
            memory[s] = f(s)
        return memory[s]

    return inner

@memoize_web_page
def read_url(url: str) -> str:
    # Code debug
    if len(url) < 20:
        with open(url, encoding="utf-8") as f:
            return f.read()

    # Some websites block default Python scripts.
    # It's good practice to identify yourself with a User-Agent header.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    # print(f"Downloading content from {url}...")

    try:
        # Make the GET request
        response = requests.get(url, headers=headers)
        # Check if the request was successful (status code 200)
        response.raise_for_status()
        # Get the content as a string
        return response.text

    except requests.exceptions.RequestException as e:
        print_error(f'*** An error occurred: {e}')
        return ''

def sanitize_filename(filename):
    """Removes invalid characters from a filename."""
    open_quotes = True
    while '"' in filename:
        filename = filename.replace('"', '«' if open_quotes else '»', 1)
        open_quotes = not open_quotes
    filename = re.sub(r'[\\/*?:"<>|]', "", filename.replace('?', '¿').replace(':', ',').replace('/', '-').replace('”', '»').replace('“', '«').replace('’', "'").replace('\xa0', ' '))
    while '  ' in filename:
        filename = filename.replace('  ', ' ')
    filename = filename.replace(' ,', ',').replace(' .', '.').replace(' ¿', '¿').replace(' !', '!').replace('« ', '«').replace(' »', '»').replace('( ', '(').replace(' )', ')')
    return filename.strip()

def process_podcast_page(path: str, episode_url: str) -> bool:
    text = read_url(episode_url)
    if text == "":
        print_error('*** Error when reading url')
        return False

    re_script = re.compile(r'<script[^>]*type="application/ld\+json">(.*?)</script>', re.MULTILINE)    # non-greedy capture
    find_iter = re_script.finditer(text)
    if find_iter:
        for ma in find_iter:
            data = ma.group(1)
            jdata = json.loads(data)
            graph = jdata.get("@graph")[0]
            # print(graph.get("@type"))
            if graph.get("@type") == "RadioEpisode":

                title: str = graph.get("name")
                date_created = datetime.fromisoformat(graph.get("dateCreated"))
                try:
                    me = graph.get("mainEntity")
                    if me is None:
                        print_error(f"*** Error: Page {episode_url} doesn't contain 'mainEntity'")
                        return False

                    url = me.get("contentUrl")
                    ext: str = url.split(".")[-1]

                    filename = path + "\\" + f"{date_created:%Y-%m-%d} - {sanitize_filename(title)}.{ext}"
                    os.makedirs(os.path.dirname(filename), exist_ok=True)

                    try:
                        # Make the request with stream=True to avoid loading the whole file in memory
                        with requests.get(url, stream=True) as r:
                            # Check if the request was successful
                            r.raise_for_status()

                            # Open the local file in binary write mode
                            with open(filename, 'wb') as f:
                                # Write the content in chunks
                                for chunk in r.iter_content(chunk_size=8192):
                                    f.write(chunk)

                        print("--> ", filename)
                        return True

                    except requests.exceptions.RequestException as e:
                        print_error(f'*** An error occurred during download: {e}')
                        return False

                except Exception as e:
                    print_error(f'*** Error during analysis: {e}')
                    return False

    print_error('*** Error: no iterator found')
    return False


def get_twenty_pages(base_url: str, page_index: int) -> list[tuple[str, str]]:
    url_with_page = f"{base_url}?page={page_index}"
    text = read_url(url_with_page)

    re_liste = re.compile(r'"(https://www.radiofrance.fr/franceinter/podcasts/([^/"]+?)/[^"]+)"')

    res: list[tuple[str, str]] = []
    find_iter = re_liste.finditer(text)
    if find_iter:
        for ma in find_iter:
            serie: str = ma.group(2)
            episode_url: str = ma.group(1)
            res.append((serie, episode_url))

    return res


if __name__ == "__main__":
    print_warning("Module pa_core is not supposed to be executed directly.")