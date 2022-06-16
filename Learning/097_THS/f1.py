import operator
import pprint
from common_fs import *

l:list = [(len(file_part(file)), file_part(file)) for file in get_all_files(r'D:\Ygg\Seeding\Mes Uplads PDF\#Bibliothèque Tangente HS All')]
l.sort(key=operator.itemgetter(0))

pprint.pprint(l)
