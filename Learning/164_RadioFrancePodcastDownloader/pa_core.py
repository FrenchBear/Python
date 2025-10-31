# pa_core.py - Core processing of Radio France podcasts
#
# 2025-10-20    PV      First version (archives download)
# 2025-10-21    PV      Version for podcast downloader

from datetime import datetime
import os
import re
import json
import requests

def read_url(url: str) -> str:
    # Code debug
    if len(url) < 20:
        with open(url, "r", encoding="utf-8") as f:
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
        print(f"*** An error occurred: {e}")
        return ""

def sanitize_filename(filename):
    """Removes invalid characters from a filename."""
    return re.sub(r'[\\/*?:"<>|]', "", filename.replace('?', '¿').replace(':', ',').replace('/', '-').replace('"', "-").replace('”', '»').replace('“', '«'))

def process_podcast_page(path: str, episode_url: str) -> bool:
    # with open("tanguy-pastureau-maltraite-l-info-du-lundi-20-octobre-2025-4645466.html", "r", encoding="utf-8") as f:
    #     text = f.read()
    text = read_url(episode_url)
    if text == "":
        print("*** Error when reading url")
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

                title = graph.get("name")
                date_created = datetime.fromisoformat(graph.get("dateCreated"))
                try:
                    if graph.get("mainEntity") == None:
                        print(f"*** Error: Page {episode_url} doesn't contain 'mainEntity'")
                        return False

                    url = graph.get("mainEntity").get("contentUrl")
                    ext = url.split(".")[-1]

                    # print("Titre:", title)
                    # print("Date:", date_created)
                    # print("Url:", url)

                    filename = path + "\\" + sanitize_filename(f"{date_created:%Y-%m-%d} - {title}.{ext}")
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    # print("Filename:", filename)

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
                        print(f'*** An error occurred during download: {e}')
                        return False

                except Exception as e:
                    print(f'*** Error during analysis: {e}')
                    return False

    print('*** Error: no iterator found')
    return False


def get_twenty_pages(page_url: str) -> list[str]:
    # with open("tp.html", "r", encoding="utf-8") as f:
    #     text = f.read()
    text = read_url(page_url)

    re_liste = re.compile(r'"(https://www.radiofrance.fr/franceinter/podcasts/([^/"]+?)/[^"]+)"')

    res = []
    find_iter = re_liste.finditer(text)
    if find_iter:
        for ma in find_iter:
            serie = ma.group(2)
            episode_url = ma.group(1)
            res.append((serie, episode_url))

    return res
