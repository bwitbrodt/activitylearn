%% Human Activity Classification example - Data Preparation Script
% This scripts helps prepare the data for the Human Classification Example.
% It must be run before executing DemoMain.m, or any of the functions used
% in there.
% 
% The dataset itself it too large to be hosted on MATALAB Central directly.
% 
% Copyright 2014-2015 The MathWorks, Inc.

%% First step - get the dataset
% The original dataset is available from the following address:
% <http://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones>
% 
% The dataset is available courtesy of:
% 
% Davide Anguita, Alessandro Ghio, Luca Oneto, Xavier Parra
% and Jorge L. Reyes-Ortiz. A Public Domain Dataset for Human Activity
% Recognition Using Smartphones. 21th European Symposium on Artificial
% Neural Networks, Computational Intelligence and Machine Learning,
% ESANN 2013. Bruges, Belgium 24-26 April 2013. 
%
% The command below helps automate the download process by opening a 
% "Save As..." system dialog directly. 
% 
% Please save the .zip archive under
% the .\Data\Original folder.

%web('http://archive.ics.uci.edu/ml/machine-learning-databases/00240/UCI HAR Dataset.zip')

%fprintf(['\nDownload of the original dataset in progress...\n',...
%    'Please allow the download of the .zip file to complete before proceeding.\n\n',...
%   'Press a key when done.\n'])
%pause

%% Second step - re-arrange relevant portions of dataset
% The function prepareData reads the total acceleration data in the
% original Human Activity Recognition dataset, re-organizes it and saves
% it in a new set of MATLAB data (.mat) files.
%
% When prompted, please point the function to the locally-saved .zip
% archive containing the dataset.
addpath('.\Data')
prepareData

%% Data preparation finished

fprintf('\nData preparation finished! You can now move on to the main demo script.\n\nOpening DemoMain.m...')
edit('DemoMain')
fprintf('Done.\n')