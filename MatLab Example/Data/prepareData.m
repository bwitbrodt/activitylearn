function prepareData()
% prepareData Extract relevant data from Human Activity Recognition dataset
% This function reads the total acceleration data in the original Human
% Activity Recognition dataset, re-organizes it and saves it in a new set
% of MATLAB data (.mat) files.
% 
% Before running this function, ensure you download the original dataset
% from:
% <http://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones>
% 
% Download "Data Folder", and save the archive under the .\Data\Original
% folder
% 
% The data in the original dataset is available courtesy of:
% 
% Davide Anguita, Alessandro Ghio, Luca Oneto, Xavier Parra
% and Jorge L. Reyes-Ortiz. A Public Domain Dataset for Human Activity
% Recognition Using Smartphones. 21th European Symposium on Artificial
% Neural Networks, Computational Intelligence and Machine Learning,
% ESANN 2013. Bruges, Belgium 24-26 April 2013. 
% 
% Copyright 2014-2015 The MathWorks, Inc.

% Path of current function
%fcnpath = mfilename('fullpath');

% Default source path for original data
%bs = strfind(fcnpath, '\');
% defaultOriginalDataPath = fullfile(fcnpath(1:bs(end)-1),'Original');
% 
% % Identify archived data file
% [sourceFilename,sourcePath] = uigetfile('*.zip',...
%     'Select the locally downloaded UCI HAR Dataset Archive',...
%     defaultOriginalDataPath);
% 
% if(~ischar(sourceFilename))
%     disp('Invalid file selection - data unzip aborted')
%     return
% end
% 
% % Unzip source archive and create nested folder with same name
% fprintf('Unzipping HAR dataset...')
% unzip(fullfile(sourcePath,sourceFilename),sourcePath)
% fprintf('Done.\n')
% 
% % Form path name of source folder:
% % Get rid of .zip extension
% foldername = sourceFilename(1:end-4);
% % Get hold of data
%sourceDataPath = fullfile(sourcePath,foldername);
sourceTrainDataPath = 'Users\gregeschelbach\Documents\activitylearn\MatLab_Example\Data\Original\train';
sourceTestDatapath = 'Users\gregeschelbach\Documents\activitylearn\MatLab_Example\Data\Original\test';

% Define destination path
%destDataPath = fullfile(fcnpath(1:bs(end)-1),'Prepared');

% Load acceleration data (Total)
%'Users/gregeschelbach/Documents/activitylearn/MatLab_Example/Data/Original/train/Inertial_Signals/body_acc_x_train.txt'
ax_train = importAccelerationComponentFile('total_acc_x_train.txt');
ay_train = importAccelerationComponentFile('total_acc_y_train.txt');
az_train = importAccelerationComponentFile('total_acc_z_train.txt');
ax_test = importAccelerationComponentFile('total_acc_x_test.txt');
ay_test = importAccelerationComponentFile('total_acc_y_test.txt');
az_test = importAccelerationComponentFile('total_acc_z_test.txt');

% Load labels - subject and activity id
s_train = importSubjectBufferList('subject_train.txt');
y_train = importClassBufferList('y_train.txt');
s_test = importSubjectBufferList('subject_test.txt');
y_test = importClassBufferList('y_test.txt');

% Concatenate acceleration
atx = [ax_train; ax_test];
aty = [ay_train; ay_test]; 
atz = [az_train; az_test]; 

% Concatenate labels - subject and activity id
subid = [s_train; s_test]; 
actid = [y_train; y_test]; 

% Create activity labels
actnames = {'Walking','WalkingUpstairs', 'WalkingDownstairs',...
    'Sitting','Standing','Laying'}; %#ok<NASGU>

% Define sample frequency (in Hz) and time vector for each buffer
fs = 50;
t = (1/fs)*(0:size(atx,2)-1); %#ok<NASGU>

% Save relevant arrays to MAT file BufferedAccelerations.mat
fprintf('Saving buffered data...')
save('BufferedAccelerations.mat',...
    'atx','aty','atz','subid','actid','actnames','fs','t')
fprintf('Done.\n')

% Buffered data saved - move on to unbuffered data
% subjects = createUnbufferedData(subid, actid, atx, aty, atz); %#ok<NASGU>
% 
% Save large structure with unbuffered data to file
% fprintf('Saving unbuffered data...')
% save(fullfile(destDataPath,'RecordedAccelerationsBySubject.mat'),...
%     'subjects','fs','actnames');
% fprintf('Done.\n')
% 
% --- Helper functions
% 
% function datastruct = createUnbufferedData(subid, bufactid, ...
%     totaldatax, totaldatay, totaldataz)
% 
% Initialize structure array - one component per subject
% datastruct = struct('actid',[],'totalacc',[]);
% 
% s = unique(subid);
% 
% Loop through subjects
% for ks = 1:length(s)
% 
%     subject = s(ks);
%     
%     fprintf('Unbuffering data for subject #%g...',subject)
%     
%     subidx = subid==subject;
%     totx = totaldatax(subidx,:);
%     toty = totaldatay(subidx,:);
%     totz = totaldataz(subidx,:);
%     aid = bufactid(subidx,:);
%     
%     [acc3d, unbufactid] = unbufferSubjectData(totx, toty, totz, aid);
%     
%     datastruct(subject).actid = unbufactid;
%     (Rescale all acelerations to real-world values before saving)
%     g = 9.80665;
%     datastruct(subject).totalacc = g * acc3d;
% 
%     fprintf('Done.\n')
%     
% end
% 
% function [acc3d, actid] = unbufferSubjectData(axbuf, aybuf, azbuf, bufactid)
% 
% if(isempty(axbuf))
%     fprintf('Warning: not enough data for subject %d\n',subjectNumber)
%     return
% end
% 
% L = size(axbuf,2);
% 
% Get rid of overlapping regions and make a single long vector
% 
% Data X
% totx = axbuf.';
% t1 = totx(1:L/2,1);
% totx(1:L/2,:) = [];
% tx = [t1;totx(:)];
% 
% Data Y
% toty = aybuf.';
% t1 = toty(1:L/2,1);
% toty(1:L/2,:) = [];
% ty = [t1;toty(:)];
% 
% Data Z
% totz = azbuf.';
% t1 = totz(1:L/2,1);
% totz(1:L/2,:) = [];
% tz = [t1;totz(:)];
% 
% Create new vector of activities id with same length
% tmp = [bufactid(1);bufactid];
% aextended = tmp * ones(1,L/2);
% actid = reshape(aextended.',[],1);
% 
% Concatenate all acceleration components together
% acc3d = [tx, ty, tz];
% 
