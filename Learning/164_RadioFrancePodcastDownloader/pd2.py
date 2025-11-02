# pd2.py
# Podcast download from France Inter Podcasts web pages
#
# 2025-10-21    PV      First version, writing core
# 2025-10-22    PV      Generic downloader
# 2025-11-02    PV      Skip serie stodio-payet

# Using curl, in case of CRYPT_E_NO_REVOCATION_CHECK (0x80092012) - The revocation function was unable to check revocation for the certificate
# use curl --ssl-no-revoke ...

import yaml
import pa_core

# import sys
# res = pa_core.process_podcast_page(r"C:\Temp", "tp31oct.html")
# sys.exit(0)

CONFIG_FILE = r"C:\MusicOD2\Podcasts\RadioFrance\configRF.yaml"

def load_config():
    """Loads the YAML configuration file."""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{CONFIG_FILE}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

def save_config(config):
    """Saves the updated configuration to the YAML file."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)


def process_podcast_main_page(podcast_config, index, total):
    """Downloads a single podcast based on its configuration."""

    podcast_title = podcast_config.get('podcast', 'Unknown Podcast')
    url = podcast_config.get('url')
    path = podcast_config.get('path')
    last_download = podcast_config.get('last_download')
    defcount = int(podcast_config.get('defcount', '3'))
    active = podcast_config.get('active', True)

    if not active:
        print(f"[{index}/{total}] Inactive: {podcast_title}")
        return

    print(f"[{index}/{total}] Processing: {podcast_title}")

    if not url or not path:
        print(f"  -> Skipping '{podcast_title}': 'url' or 'path' is missing.")
        return

    page_count = -1
    twenty_pages = pa_core.get_twenty_pages(url)
    for ix, (_, page) in enumerate(twenty_pages):
        if page == last_download:
            page_count = ix
            break
    if page_count == 0:
        print("--> No new poadcast\n")
        return
    if page_count == -1:
        print(f"Can't find last downloaded page, will load top {defcount} pages")
        page_count = defcount
    else:
        print(f"--> {page_count} podcasts to load")

    res = True
    for ix in range(page_count):
        if twenty_pages[ix][0] != 'studio-payet':       # untested
            if not pa_core.process_podcast_page(path.replace("{serie}", twenty_pages[ix][0]), twenty_pages[ix][1]):
                res = False
                break

    ############################
    # ToDo: In case of problem in podcast_process_page, don't update config !!!!

    # Works because podcast_config is actually a reference in outer config
    if res:
        podcast_config['last_download'] = twenty_pages[0][1]
        save_config(config)
    else:
        print("Errors during podcast processing, history not updated")
    print()


if __name__ == "__main__":
    config = load_config()
    if config and 'podcasts' in config:
        podcasts_list = config['podcasts']
        total_podcasts = len(podcasts_list)
        print(f"Found {total_podcasts} podcasts to check.\n")

        for i, podcast_conf in enumerate(podcasts_list):
            process_podcast_main_page(podcast_conf, i + 1, total_podcasts)

