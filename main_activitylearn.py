#Main Program
#I'm starting this as the main program where we will call all of the other functions and run from
#So start adding things here as they are finished

#BEFORE RUNNING:
#1.) make sure you point the variables below towards your files
#2.)recommend restarting the python kernal to clear all the memory: run-->restart kernal

import prepareData as prd
import extractAllFeatures as eaf
import featuresFromBuffer as ffb


#make these variables point to where you are keepign the data files
#NOTE there is some weirdness going on in python with the open() function, it randomly inserts 'extra' "\" into the file path.
#you will note that I had to manually go through an put extra "\"s in teh file paths to make it work. Weird. But it works.

#body xacc train
bxtr = open('C:\Users\Brad\\activity\\activitylearn\data\\train\Inertial Signals\\body_acc_x_train.txt','r')
#body yacc train 
bytr = open('C:\Users\Brad\\activity\\activitylearn\data\\train\Inertial Signals\\body_acc_y_train.txt','r')
#body xacc train
bztr = open('C:\Users\Brad\\activity\\activitylearn\data\\train\Inertial Signals\\body_acc_z_train.txt','r')
#body xacc test
bxte = open('C:\Users\Brad\\activity\\activitylearn\data\\test\Inertial Signals\\body_acc_x_test.txt','r')
#body yacc test
byte = open('C:\Users\Brad\\activity\\activitylearn\data\\test\Inertial Signals\\body_acc_y_test.txt','r')
#body zacc test
bzte = open('C:\Users\Brad\\activity\\activitylearn\data\\test\Inertial Signals\\body_acc_z_test.txt','r')
#subject train
subtr =  open('C:\Users\Brad\\activity\\activitylearn\data\\train\subject_train.txt','r')
#y_train
ytr = open('C:\Users\Brad\\activity\\activitylearn\data\\train\y_train.txt','r')
#subject test
subte = open('C:\Users\Brad\\activity\\activitylearn\data\\test\subject_test.txt','r')
#body xacc test
#y_test
yte = open('C:\Users\Brad\\activity\\activitylearn\data\\test\y_test.txt','r')


#prepare the above data files
prd.prepareData(bxtr, bytr, bztr,bxte,byte,bzte,subtr,ytr,subte,yte)
print 'data prepared successfully'

## Ok works up until here so far
## starting on next step