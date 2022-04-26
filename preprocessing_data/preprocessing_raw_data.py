import os, re, shutil
from os import path
import pandas as pd
from pandas.errors import EmptyDataError

source_path = 'D:\\Project\\Bird detection\\data'
dest_path = 'D:\\Project\\Bird detection\\preprocess_bird_data'
label_path = 'D:\\Project\\Bird detection\\Label\\predefined_classes.txt'

columns = ['classes', 'x', 'y', 'w', 'h', 'filename']

# combine raw_data and web_raw_data into one raw data and rename all files
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

# perform value counts on each classes and export csv file for train test split for training purpose
def count_classes():
    data_list = pd.DataFrame()
    for filename in os.listdir(dest_path):
        if filename.endswith('.txt'):
            try:
                tmp = pd.read_csv(os.path.join(dest_path, filename), sep=' ', header=None)
                tmp = pd.DataFrame(tmp)
                tmp['filename'] = str(filename.split('.')[0])
                data_list = pd.concat([data_list, tmp], axis=0, ignore_index=True)
            except EmptyDataError:
                print('File without any label: ' + filename)
    
    data_list.columns = columns
    
    # create csv file fro classes counts
    count = data_list['classes'].value_counts().rename_axis('classes').reset_index(name='counts')
    label = pd.read_csv(label_path, header=None).to_dict()[0]
    count['classes'] = count['classes'].replace(label)
    count.to_csv('total_bird_count.csv',index=False)
    
    # create csv file for train test split file
    data_list['classes'] = data_list['classes'].replace(label)
    train_test_split = data_list.groupby(['filename', 'classes']).size().reset_index(name='counts')
    train_test_split.to_csv('train_test_split_list_count.csv', index=False)



if __name__ == '__main__':
    # Create dictionary to save the number
    bird_pic_count = {}
    filename_list = os.listdir(source_path)
    for file in filename_list:
        subfiles = os.path.join(source_path, file)
        for subfile in os.listdir(subfiles):
            subfile = os.path.join(subfiles, subfile)
            convert_filename(subfile)
    
    count_classes()
