import os, shutil
from os import path
import pandas as pd
from pandas.errors import EmptyDataError

source_path = 'D:\\Project\\Bird detection\\preprocess_bird_data'
label_path = 'D:\\Project\\Bird detection\\Label\\predefined_classes.txt'

columns = ['classes', 'x', 'y', 'w', 'h', 'filename']

def count_classes():
    data_list = pd.DataFrame()
    for filename in os.listdir(source_path):
        if filename.endswith('.txt'):
            try:
                tmp = pd.read_csv(os.path.join(source_path, filename), sep=' ', header=None)
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
    count_classes()
