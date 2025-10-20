# pd.py - Podcasts downloader
#
# 2025-10-20    PV      Code written by Gemini

# I want to build a python program to download podcasts audio or video files on Windows.
# 
# This program should be configured by a yaml file, a list of records describing each one a podcast, such as:
# 
# - podcast: Tanguy Pastureau maltraite l'info
# - url: https://radiofrance-podcast.net/podcast09/rss_18141.xml
# - path: D:\Temp\Podcasts\Tanguy Pastureau
# - last_download: <date time>
# 
# - podcast: Charline explose les faits
# - url: https://radiofrance-podcast.net/podcast09/rss_13129.xml
# - path: D:\Temp\Podcasts\Charline Vanhoenacker
# - last_download: <date time>
# 
# Each podcast contains folloging information: podcast: a title, to be displayed to indicate progress when downloading
# url: the RSS feed of the podcast path: local folder in which media files should be stored, to be created if it doesn't
# exist last_download: a timestamp of the most recent podcast dowloaded, so during a download operation, analysis of RSS
# feed will not examine older podcasts. This field should be updated after a successful download operation. If this
# field doesn't exists or is empty, then all feeds should be downloaded.
# 
# Podcasts should be downloaded from last_download date to the most recent, and last_downloaded field updated after each
# download, so if downloads stops for any reason, restarting it will continue where it has been interrupted.
# 
# Finally, I want to rename the downloaded media file. By default, media file has a unreadable name such as
# "13129-20.10.2025-ITEMA_24284340-2025F21436S0293-NET_MFI_C3CDD91E-20E8-4C07-80CD-2FA43969CCE5.mp3" but I prefer a much
# more readable, based on "date - title.ext" such as "2025-10-20 - Le QCM pour devenir français, cadeau de départ de
# Retailleau.mp3" in this specific example.

import yaml
import feedparser
import requests
import os
from datetime import datetime, timezone
import re

CONFIG_FILE = 'config.yaml'

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

def sanitize_filename(filename):
    """Removes invalid characters from a filename."""
    return re.sub(r'[\\/*?:"<>|]', "", filename.replace('?','¿').replace(':',',').replace('/','-'))

def download_podcast(podcast_config, index, total):
    """Downloads a single podcast based on its configuration."""
    podcast_title = podcast_config.get('podcast', 'Unknown Podcast')
    url = podcast_config.get('url')
    path = podcast_config.get('path')
    last_download_str = podcast_config.get('last_download')

    print(f"[{index}/{total}] Processing: {podcast_title}")

    if not url or not path:
        print(f"  -> Skipping '{podcast_title}': 'url' or 'path' is missing.")
        return

    # Create directory if it doesn't exist
    os.makedirs(path, exist_ok=True)

    # Parse the RSS feed
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"  -> Error fetching feed for '{podcast_title}': {e}")
        return

    # Get the last download time
    last_download_dt = None
    if last_download_str:
        try:
            # Assume ISO 8601 format, make it timezone-aware (UTC)
            last_download_dt = datetime.fromisoformat(last_download_str).replace(tzinfo=timezone.utc)
        except ValueError:
            print(f"  -> Warning: Invalid date format for 'last_download' in '{podcast_title}'. Will download all.")

    # Sort entries from oldest to newest to download in chronological order
    sorted_entries = sorted(feed.entries, key=lambda x: x.get('published_parsed'))  # type: ignore

    new_episodes_downloaded = 0
    for entry in sorted_entries:
        entry_title = entry.get('title', 'No Title')
        published_time = entry.get('published_parsed')

        if not published_time:
            print(f"  -> Skipping episode '{entry_title}': No publication date.")
            continue

        # Convert published_time to a timezone-aware datetime object (assuming UTC)
        entry_dt = datetime(*published_time[:6], tzinfo=timezone.utc)

        # Download if it's newer than the last download
        if not last_download_dt or entry_dt > last_download_dt:
            media_url = None
            file_ext = '.mp3' # Default extension
            for link in entry.get('links', []):
                if link.get('rel') == 'enclosure':
                    media_url = link.get('href')
                    # Try to get a better file extension
                    if '.' in media_url.split('/')[-1]:
                        file_ext = '.' + media_url.split('.')[-1]
                    break

            if media_url:
                date_str = entry_dt.strftime('%Y-%m-%d')
                new_filename = sanitize_filename(f"{date_str} - {entry_title}{file_ext}")
                filepath = os.path.join(path, new_filename)

                if os.path.exists(filepath):
                    print(f"  -> Already exists: '{new_filename}'")
                else:
                    print(f"  -> Downloading: '{new_filename}'")
                    try:
                        response = requests.get(media_url, stream=True)
                        response.raise_for_status()
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        # Update config immediately after successful download
                        podcast_config['last_download'] = entry_dt.isoformat()
                        save_config(config)
                        new_episodes_downloaded += 1

                    except requests.exceptions.RequestException as e:
                        print(f"    -> FAILED to download '{new_filename}': {e}")
                        # Stop processing this podcast if a download fails
                        return
    
    if new_episodes_downloaded == 0:
        print("  -> No new episodes to download.")


if __name__ == "__main__":
    config = load_config()
    if config and 'podcasts' in config:
        podcasts_list = config['podcasts']
        total_podcasts = len(podcasts_list)
        print(f"Found {total_podcasts} podcasts to check.\n")
        
        for i, podcast_conf in enumerate(podcasts_list):
            download_podcast(podcast_conf, i + 1, total_podcasts)
            print("-" * 20)
            
        print("\nAll podcasts processed.")
