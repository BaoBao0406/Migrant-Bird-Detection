import os, shutil
from os import path
import pandas as pd
import numpy as np
from pathlib import Path


df = pd.read_csv('process_train_test_split_list_count.csv')


# preprocess test label data
df['train_test_split'] = df['train_test_split'].fillna(0).astype(float).astype(int)
share_test_label = df[df['train_test_split'] == 1]
share_test_filename = share_test_label['filename'].to_list()
df['train_test_split'] = np.where(df['filename'].isin(share_test_filename), 1, 0)

# Join the current path with the photo path
#filepath = os.path.join(Path(__file__).parent.parent, 'preprocess_bird_data\\')
# filepath for darknet
filepath = 'data\\bird_data\\'
df['filename'] = filepath + df['filename'] + str('.jpg')


# Number of test sample
test = df[df['train_test_split'] == 1]
test_count = test.groupby(['classes'])['counts'].sum().reset_index(name='test_count').sort_values('test_count')

# Number of training sample
train = df[df['train_test_split'] == 0]
train_count = train.groupby(['classes'])['counts'].sum().reset_index(name='train_count').sort_values('train_count')


train_test_portion = test_count['test_count'] / (test_count['test_count'] + train_count['train_count']) * 100

train_test_split_data = pd.concat([train_count, test_count, train_test_portion], axis=1)

# Check for train test proportion
# print(train_test_split_data)


# Export train and test filepath to txt
train['filename'].to_csv('train.txt', index=False, header=False)
test['filename'].to_csv('test.txt', index=False, header=False)




