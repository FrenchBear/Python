from common_fs import get_all_files, file_size
from common_pdf import pdf_numpages


source = r'W:\TempBD\final'


with open('pdf_size_pages.txt', 'w', encoding='utf-8') as out:
    for filefp in get_all_files(source):
        try:
            pages = pdf_numpages(filefp)
            if pages>=4:
                length = file_size(filefp)
                ratio = length//pages
                print(f"{filefp:<80} {pages:>4}   {'{:_}'.format(length).replace('_', ' ').rjust(13)}     {'{:_}'.format(ratio).replace('_', ' ').rjust(11)}")
                out.write(f'{length};{pages};{ratio};{filefp}\n')
                out.flush()
        except:
            pass
