# pa_daniel_morin.py - Podcasts Archives (Radio France), Daniel Morin
#
# 2025-10-20    PV      First version

from datetime import datetime
import re
import json
import requests

def read_url(url: str) -> str:
    # Some websites block default Python scripts. 
    # It's good practice to identify yourself with a User-Agent header.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    #print(f"Downloading content from {url}...")

    try:
        # Make the GET request
        response = requests.get(url, headers=headers)
        # Check if the request was successful (status code 200)
        response.raise_for_status()
        # Get the content as a string
        return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise e

def sanitize_filename(filename):
    """Removes invalid characters from a filename."""
    return re.sub(r'[\\/*?:"<>|]', "", filename.replace('?','¿').replace(':',',').replace('/','-'))

def process_episode(episode_url: str):
    # with open("le-billet-de-daniel-morin-du-mercredi-01-mars-2023-9733913.html", "r", encoding="utf-8") as f:
    #     text = f.read()

    text = read_url(episode_url)

    re_script = re.compile(r'<script[^>]*type="application/ld\+json">(.*?)</script>', re.MULTILINE)    # non-greedy capture
    find_iter = re_script.finditer(text)
    if find_iter:
        for ma in find_iter:
            data = ma.group(1)
            jdata = json.loads(data)
            graph = jdata.get("@graph")[0]
            #print(graph.get("@type"))
            if graph.get("@type")=="RadioEpisode":
                #print("RadioEpisode found")

                title = graph.get("name")
                date_created = datetime.fromisoformat(graph.get("dateCreated"))
                url = graph.get("mainEntity").get("contentUrl")
                ext = url.split(".")[-1]

                # print("Titre:", title)
                # print("Date:", date_created)
                # print("Url:", url)

                filename = "C:\\downloads\\" + sanitize_filename(f"{date_created:%Y-%m-%d} - {title}.{ext}")
                #print("Filename:", filename)

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

                except requests.exceptions.RequestException as e:
                    print(f"An error occurred during download: {e}")


def process_page(page_url: str):
    # with open("p23.html", "r", encoding="utf-8") as f:
    #     text = f.read()
    text = read_url(page_url)

    re_liste = re.compile(r'"(https://www.radiofrance.fr/franceinter/podcasts/le-billet-de-daniel-morin/[^"]+)"')

    find_iter = re_liste.finditer(text)
    if find_iter:
        for ma in find_iter:
            episode_url = ma.group(1)
            print(episode_url)
            process_episode(episode_url)


# Page 30 not downloaded yet
process_page("https://www.radiofrance.fr/franceinter/podcasts/le-billet-de-daniel-morin?p=30")
