# pd2.py
# Podcast download from France Inter Podcasts web pages
#
# 2025-10-21    PV      First version, writing core
# 2025-10-22    PV      Generic downloader
# 2025-11-02    PV      Skip serie stodio-payet
# 2025-11-05    PV      Look for last downloaded episoze in the last 5 main pages; use memoization
# 2025-11-19    PV      Bug when last episode was first of a page other than 1 fixed
# 2025-12-29    PV      Errors in red to be more visible
# 2026-02-14    PV      Added ignore list to avoid duplicate loading in L'humour d'Inter

# Using curl, in case of CRYPT_E_NO_REVOCATION_CHECK (0x80092012) - The revocation function was unable to check revocation for the certificate
# use curl --ssl-no-revoke ...

import yaml
import pa_core
from pa_core import print_error, print_warning

CONFIG_FILE = r"C:\MusShared\Podcasts\RadioFrance\configRF.yaml"

def load_config():
    """Loads the YAML configuration file."""
    try:
        with open(CONFIG_FILE, encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print_error(f"*** Error: Configuration file '{CONFIG_FILE}' not found.")
        return None
    except yaml.YAMLError as e:
        print_error(f"*** Error parsing YAML file: {e}")
        return None

def save_config(config):
    """Saves the updated configuration to the YAML file."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)


def process_podcast_main_page(podcast_config, index, total):
    """Downloads podcasts for a specific group, knowing the last downloaded page."""

    podcast_title = podcast_config.get('podcast', 'Unknown Podcast')
    url = podcast_config.get('url')
    path = podcast_config.get('path')
    last_download = podcast_config.get('last_download')
    defcount = int(podcast_config.get('defcount', '3'))
    ignore = podcast_config.get('ignore', [])
    active = podcast_config.get('active', True)

    if not active:
        print(f"[{index}/{total}] Inactive: {podcast_title}")
        return

    print(f"[{index}/{total}] Processing: {podcast_title}")

    if not url or not path:
        print_warning(f"  -> Skipping '{podcast_title}': 'url' or 'path' is missing.")
        return

    # Determine page_index and expsode_index of the first episode to download (included),
    # until episode_index 1 of episode_page 1

    page_index = 1
    episode_index = -1

    while True:
        twenty_pages = pa_core.get_twenty_pages(url, page_index)
        for ix, (_, page) in enumerate(twenty_pages):
            if page == last_download:
                episode_index = ix
                break

        if episode_index == 0 and page_index == 1:
            print_warning("--> No new poadcast\n")
            return

        if episode_index == -1:
            if page_index == 5:
                print(f"Can't find last downloaded episode in the first 5 pages, will load top {defcount} episodes of page 1")
                breakpoint()    # to debug why not found
                page_index = 1
                episode_index = defcount - 1
                break
            # Not found on current page, continue with next page
            page_index += 1
        else:
            print(f"Start downloading from page {page_index} episode {episode_index}")
            break

    episode_index -= 1
    for p in range(page_index, 0, -1):
        print(f"Processing page {p}")
        twenty_pages = pa_core.get_twenty_pages(url, p)
        res = True
        for ix in range(episode_index, -1, -1):
            if twenty_pages[ix][0] != 'studio-payet' and not twenty_pages[ix][0] in ignore:
                if not pa_core.process_podcast_page(path.replace("{serie}", twenty_pages[ix][0]), twenty_pages[ix][1]):
                    res = False
                    break
        if not res:
            break
        # In case we continue with previous page contating a slice of 20 episodes
        episode_index = 19

    # If there was a problem, don't update config
    # Works because podcast_config is actually a reference in outer config
    if res:
        podcast_config['last_download'] = twenty_pages[0][1]
        save_config(config)
    else:
        print_error("*** Errors during podcast processing, history not updated")
    print()


if __name__ == "__main__":
    config = load_config()
    if config and 'podcasts' in config:
        podcasts_list = config['podcasts']
        total_podcasts = len(podcasts_list)
        print(f"Found {total_podcasts} podcasts to check.\n")

        for i, podcast_conf in enumerate(podcasts_list):
            process_podcast_main_page(podcast_conf, i + 1, total_podcasts)
