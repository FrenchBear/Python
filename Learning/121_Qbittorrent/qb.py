# qBittorrent API
# 2023-01-28    PV
#
# https://qbittorrent-api.readthedocs.io/en/latest/index.html
# pip install qbittorrent-api

import qbittorrentapi
from common_fs import file_exists, file_readalltext
import os
import shutil

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(
    host='thor',
    port=8080,
    username='admin',
    password=file_readalltext(r'C:\Utils\Local\qbittorrent.txt')
 )


# The Client will automatically acquire/maintain a logged in state in line with any request.
# Therefore, this is not necessary; however, you many want to test the provided login credentials.
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

# display qBittorrent info
#print(f'qBittorrent: {qbt_client.app.version}')
#print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')
#for k,v in qbt_client.app.build_info.items(): print(f'{k}: {v}')

# retrieve and show all torrents
for torrent in qbt_client.torrents_info():
    #print(f'{torrent.hash[-6:]}: {torrent.name} ({torrent.state})')
    # for k, v in torrent.items():
    #     print(f"  {k}: {v}")
    
    # if torrent["save_path"]==r'D:\Ygg\Seeding\Mes Uplads PDF':
    #     tfcandidate = os.path.join(r'\\thor\ygg\Torrents Seeding', torrent["name"]+'.torrent')
    #     if not file_exists(tfcandidate):
    #         tfcandidate = os.path.join(r'\\thor\ygg\Torrents Seeding', stem_part(torrent["name"])+'.torrent')
    #     if file_exists(tfcandidate):
    #         print(torrent["name"])
    #         shutil.copy(tfcandidate, r'C:\Users\Pierr\Desktop\MyTorrents')
    #         torrent.set_location(location=r'\\teraz\torrents\downloads\!MyUploadsPDF')

    if torrent["save_path"]==r'D:\Ygg\Seeding\Livres info':
        tfcandidate = os.path.join(r'\\thor\ygg\Torrents Seeding', torrent["name"]+'.torrent')      # type: ignore
        if file_exists(tfcandidate):
            print(torrent["name"])
            shutil.copy(tfcandidate, r'C:\Users\Pierr\Desktop\MyTorrents')
            torrent.set_location(location=r'\\teraz\torrents\downloads')
