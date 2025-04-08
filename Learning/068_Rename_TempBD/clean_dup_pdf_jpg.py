import os


source = r"W:\TempBD\archives"
DO_IT = True


for root, subs, files in os.walk(source, False):
    for file in files:
        stem, ext = os.path.splitext(file)
        if ext.lower() == ".pdf":
            imagefilefp = os.path.join(root, stem + ".jpg")
            if os.path.exists(imagefilefp):
                print(f'del "{imagefilefp}"')
                if DO_IT:
                    os.remove(imagefilefp)
