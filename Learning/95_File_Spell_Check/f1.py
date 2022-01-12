from common_fs import *

with open(r'c:\temp\source.txt', 'w', encoding='utf-8') as fout:
    for filefp in get_all_files(r'W:\livres'):
        if not r'W:\livres\Langues\Norvégien\Audio' in filefp and not 'EC-Council Certified Ethical Hacker' in filefp and not 'Nathan SVT Term S spécifique - 2012' in filefp and not 'Le Coréen sans peine audio' in filefp:
            fout.write(filefp+'\n')
print('Done.')
