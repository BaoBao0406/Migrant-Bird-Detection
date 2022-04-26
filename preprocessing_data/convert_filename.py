import os, re
from os import path
import shutil

source_path = 'D:\\Project\\Bird detection\\data'
dest_path = 'D:\\Project\\Bird detection\\preprocess_bird_data'


def convert_filename(file_path):
    file_format = str(os.path.basename(file_path))
    file_format = re.sub('[^a-zA-Z0-9 \n\.]', '_', file_format)
    file_format = re.sub(' ', '_', file_format)
    
    bird_pic_count.setdefault(file_format, 1)
        
    for filename in os.listdir(file_path):
        if (filename.lower()).endswith('.jpg'):
            
            file_count = str(bird_pic_count[file_format]).zfill(4)
            
            
            jpg_filename = file_format + '_' + str(file_count) + '.jpg'
            txt_filename = file_format + '_' + str(file_count) + '.txt'
            
            new_filename = filename.split('.')[0]
            
            # change jpg filename
            shutil.copy(os.path.join(file_path, new_filename + '.jpg'), dest_path)
            dst_file = os.path.join(dest_path, new_filename + '.jpg')
            os.rename(dst_file, os.path.join(dest_path, jpg_filename))
            
            # change txt filename
            shutil.copy(os.path.join(file_path, new_filename + '.txt'), dest_path)
            dst_txt = os.path.join(dest_path, new_filename + '.txt')
            os.rename(dst_txt, os.path.join(dest_path, txt_filename))
            bird_pic_count[file_format] += 1

if __name__ == '__main__':
    # Create dictionary to save the number
    bird_pic_count = {}
    
    filename_list = os.listdir(source_path)
    for file in filename_list:
        subfiles = os.path.join(source_path, file)
        for subfile in os.listdir(subfiles):
            subfile = os.path.join(subfiles, subfile)
            convert_filename(subfile)
