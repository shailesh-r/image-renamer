from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import sys
import os
import shutil
import hashlib

def get_file_name(file_path):
    try:
        with Image.open(file_path) as img:
            fname = img.getexif()[306].replace(':','-').replace(' ','_')
            if fname == '0000-00-00_00-00-00': fname = None 
    except Exception as e:
            fname = None

    return(fname)

def save_file(src_file, dest_file):
    if not os.path.isfile(f'{dest_file}.jpg'):
        shutil.move(src_file, f'{dest_file}.jpg')
        # print(f'{src_file} --> {dest_file}.jpg')
        return True
    else:
        if get_md5_checksum(src_file) == get_md5_checksum(f'{dest_file}.jpg'):
            os.remove(src_file)
            print(f'deleted {src_file}')
            return True
        else:
            return False

def get_md5_checksum(file):
    md5_hash = hashlib.md5()
    md5_hash.update(open(file, 'rb').read())
    return md5_hash.hexdigest()

def main():
    src_dir  = 'E:/Photos/process/'
    dest_dir = 'E:/Photos/_Fixed/_Final_Images/'
    lst = []
    file_list = list(Path(src_dir).rglob('*.[Jj][Pp][Gg]'))
    print(len(file_list))

    for file in file_list:
        try:
            stub = get_file_name(file)
            if stub != None:
                new_name = f'{dest_dir}{stub}'
                n_name = new_name
                i = 0
                while not save_file(file, n_name):
                    i += 1
                    n_name = f'{new_name}_{i}'
        except Exception as e:
            print(f'{file}: {e}')

if __name__ == '__main__':
    main()