# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 17:29:11 2020

@author: denni
"""

import os
import pandas
import csv
import os.path
from os import path

# Start with changing working directory to where the pokemon csv file is located

cwd = os.getcwd()
cwd
os.chdir("C:/Users/denni/Documents/pokemon-images-and-types")


import shutil , random

# Deletes everything already in the test folder. Done to create a fresh set of randomized pictures.

folder = 'C:/Users/denni/Documents/pokemon-images-and-types/images/test'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))            

# Creates a test folder in test folder where the pokemon types will be divided into folders

try:
    os.mkdir('C:/Users/denni/Documents/pokemon-images-and-types/images/test/test')
except OSError:
    print("Creation failed")

# Deletes everything in the test/test folder. May not be necessary as it was just created.
    
folder = 'C:/Users/denni/Documents/pokemon-images-and-types/images/test/test'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Deletes everything already in the train folder. Done to create a fresh set of randomized pictures.

folder = 'C:/Users/denni/Documents/pokemon-images-and-types/images/train'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))            

# Creates a train folder in train folder where the pokemon types will be divided into folders

try:
    os.mkdir('C:/Users/denni/Documents/pokemon-images-and-types/images/train/train')
except OSError:
    print("Creation failed")
        
# Deletes everything in the train/train folder. May not be necessary as it was just created.    

folder = 'C:/Users/denni/Documents/pokemon-images-and-types/images/train/train'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Extracting all types from csv file and putting them into a list

Type = pandas.read_csv("pokemon.csv")
folders_to_be_made = list(set(Type.Type1.tolist()))

# Folders paths

folder = 'C:/Users/denni/Documents/pokemon-images-and-types/images/images'
train_folder = 'C:/Users/denni/Documents/pokemon-images-and-types/images/train'
test_folder = 'C:/Users/denni/Documents/pokemon-images-and-types/images/test'

# Variable created to keep count of number of times for loop is run 

pokelength=0

# For loop that puts all pokemon images into training folder.

for filename in os.listdir(folder):
        file_path = os.path.join(folder,filename)
        try:
            shutil.copy(file_path,train_folder)
            pokelength = pokelength+1
        except Exception as e:
            print('Failed to copy %s. Reason: %s' % (file_path, e))

# Randomly sample about 30 percent of the pokemon images in training folder then move them into test folder

filenames = random.sample(os.listdir(folder), round(pokelength*.3))
for fname in filenames:
    srcpath = os.path.join(train_folder, fname)
    shutil.move(srcpath, test_folder)            
            
# Changing working directory

os.chdir("C:/Users/denni/Documents/pokemon-images-and-types/images/test")

# For loop that creates type folders

for folder in os.listdir('.'):
    if os.path.isdir(folder):
        filepath = os.path.join(os.getcwd(), folder)
        l2 = os.listdir(filepath)
        for i in folders_to_be_made:     
            if i not in l2:            #Check if folder is in dir. if not create
                os.mkdir(os.path.join(filepath , i)) 


csv_file = "pokemon.csv"
existing_path_prefix = "C:/Users/denni/Documents/pokemon-images-and-types/images/test/"
new_path_prefix =[""]

for item in folders_to_be_made:
    if item!=0: new_path_prefix.append ("C:/Users/denni/Documents/pokemon-images-and-types/images/test/test/"+item)

# Changing working directory
    
os.chdir("C:/Users/denni/Documents/pokemon-images-and-types")

# Loop that takes rows in pokemon.csv and checks them against the images. It then puts the pokemon into the appropriate type folder.

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            pass    # Skip header row
        else:
            filename, type1 = row
            filepath= existing_path_prefix+"test/"+ type1
            if path.exists(existing_path_prefix+filename+".png"):#file is a png file
                try:
                    if path.exists(existing_path_prefix+ filename+".png"): #png file is in the test folder                
                        new_filename = filepath+"/"+ filename+".png"
                        old_filename = existing_path_prefix+ filename+".png"
                        shutil.copy(old_filename, new_filename)
                except Exception as e:
                    print('Failed to copy %s. Reason: %s' % (new_filename, e))
            else:
                try:
                    if path.exists(existing_path_prefix+ filename+".jpg"): #jpg file is in the test folder
                        jpg_new_filename = filepath+"/"+ filename+".jpg"
                        jpg_old_filename = existing_path_prefix+ filename+".jpg"
                        shutil.copy(jpg_old_filename, jpg_new_filename)
                except Exception as e:
                    print('Failed to copy %s. Reason: %s' % (jpg_new_filename, e))


# Repating the same thing for the images in the train folders and the train/train folders.

os.chdir("C:/Users/denni/Documents/pokemon-images-and-types/images/train")


for folder in os.listdir('.'):
    if os.path.isdir(folder):
        filepath = os.path.join(os.getcwd(), folder)
        l2 = os.listdir(filepath )
        for i in folders_to_be_made:     
            if i not in l2:            #Check if folder is in dir. if not create
                os.mkdir(os.path.join(filepath , i)) 


csv_file = "pokemon.csv"
existing_path_prefix = "C:/Users/denni/Documents/pokemon-images-and-types/images/train/"
new_path_prefix =[""]

for item in folders_to_be_made:
    if item!=0: new_path_prefix.append ("C:/Users/denni/Documents/pokemon-images-and-types/images/train/train/"+item)

cwd = os.getcwd()
os.chdir("C:/Users/denni/Documents/pokemon-images-and-types")
cwd

# Loop that takes rows in pokemon.csv and checks them against the images. It then puts the pokemon into the appropriate type folder.

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            pass    # Skip header row
        else:
            filename, type1 = row
            filepath= existing_path_prefix+"train/"+ type1
            if path.exists(existing_path_prefix+filename+".png"):#file is a png file
                try:
                    if path.exists(existing_path_prefix+ filename+".png"): #png file is in the train folder                
                        new_filename = filepath+"/"+ filename+".png"
                        old_filename = existing_path_prefix+ filename+".png"
                        shutil.copy(old_filename, new_filename)
                except Exception as e:
                    print('Failed to copy %s. Reason: %s' % (new_filename, e))
            else:
                try:
                    if path.exists(existing_path_prefix+ filename+".jpg"): #jpg file is in the train folder
                        jpg_new_filename = filepath+"/"+ filename+".jpg"
                        jpg_old_filename = existing_path_prefix+ filename+".jpg"
                        shutil.copy(jpg_old_filename, jpg_new_filename)
                except Exception as e:
                    print('Failed to copy %s. Reason: %s' % (jpg_new_filename, e))
            
            
            
            