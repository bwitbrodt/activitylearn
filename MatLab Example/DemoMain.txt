%% Human Activity Classification based on Smartphone Sensor Signals
% 
% Copyright 2014-2015 The MathWorks, Inc.

%% Introduction
% This example describes an analysis approach on accelerometer signals
% captured with a smartphone. The smartphone is worn by a subject during 6
% different types of physical activity. 
% The goal of the analysis is to build an algorithm that automatically
% identifies the activity type given the sensor measurements. 
%
% The example uses data from a recorded dataset, courtesy of:
%  Davide Anguita, Alessandro Ghio, Luca Oneto, Xavier Parra and Jorge L.
%  Reyes-Ortiz. Human Activity Recognition on Smartphones using a
%  Multiclass Hardware-Friendly Support Vector Machine. International
%  Workshop of Ambient Assisted Living (IWAAL 2012). Vitoria-Gasteiz,
%  Spain. Dec 2012
%
% The original dataset is available from
% <http://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones>

%% Check data availability
% The data need to be prepared prior to running the code in the rest of
% this script.
% To prepare the data run the script DataPreparation.m first. That guides
% through the process of downloading the data and preparing it for this
% example.
% 
% At the end of the process, the folder .\Data\Prepared must contain
% the following four data files:
% 
% * BufferedAccelerations.mat
% * BufferFeatures.mat
% * RecordedAccelerationsBySubject.mat
% * TrainedNetwork.mat

% Check that the prepared data is available, and add the data folder to
% the MATLAB search path
if ~isAllPreparedDataAvailable
    disp('Some prepared data is not yet available. Please run DataPreparation.m first')
end

%% Objective of the example
% Let's take a look at what our final result may look like. This will give
% us a better feel for what we are trying to achieve.
% For the time being you do not need to understand how this is realized

runTrainedNetworkOnBufferedData

%% Open full "recording" for a single subject (e.g. #1)

% Use a custom function to retrieve a single acceleration component for a
% particular subject.
[acc, actid, actlabels, t, fs] = getRawAcceleration('SubjectID',1,...
    'Component','x');

plot(t,acc)

%% A more detailed look into the data
% Let's look at the same data, colored based on the activity type.
% Given this data:
% 
% * We would like to be able to tell the difference between the different
%   activities, just based on the content of the signal. 
% * Note in this case the coloring is based on existing knowledge (actid)
% * Labeled data can be used to "train" a classification algorithm so it
%   can it later predict the class of new (unlabeled) data. 

% Visualize the same signal using a custom plotting function, which also
% uses the information in actid
plotAccelerationColouredByActivity(t, acc, actid, {'Vertical acceleration'})

%% First type of characterization - amplitude only
% Looking only at the raw values irrespective or their position is time can
% provide a first set of clues

%% First example - Using a mean measure
% This can easily help separate e.g. Walking from Laying
figure
plotCompareHistForActivities(acc, actid,'Walking', 'Laying')

%% Second example - Using an RMS or standard deviation measure
% This can help separate things like e.g. Walking and Standing
plotCompareHistForActivities(acc, actid,'Walking', 'Standing')

%% What next? Amplitude-only methods are often not enough
% For example it would be very hard to distinguish between
% simply Walking and WalkingUpstairs (very similar statistical moments)
% 
% An initial conclusion is that simple statistical analysis is often not
% sufficient. 
% For signals one should also consider methods that measure signal
% variations over time

plotCompareHistForActivities(acc, actid,'Walking', 'WalkingUpstairs')

%% Time-domain analysis - preliminary considerations
% There two main different types of causes behind our signals: 
% 
% * One to do with "fast" variations over time, due to body
%   dynamics (physical movements of the subject)
% * The other, responsible for "slow" variations over time, due to the
%   position of the body with respect to the vertical gravitational field
%
% As we focus on classifying the physical activities, we should focus
% time-domain analysis on the effects of body movements. These are 
% responsible for the most "rapid" (or frequent) variations in our signal.
% 
% In this specific case a simple average over a period of time would
% easily estimate the gravitational component, which could be then
% subtracted from the relevant samples to obtain the signal due to the
% physical movements.
% 
% For the sake of generality here we introduce an approach based on
% digital filters, which is much more general and can be reused in more
% challenging situations.

%% Digital filtering workflow
% To isolate the rapid signal variations from the slower ones using digital
% filtering:
% 
% * Design a high-pass filter (e.g. using the Filter Design and Analysis
%   Tool, fdatool, in MATLAB)
% * Apply the filter to the original signal

%% Filter out gravitational acceleration
% As well as interactively, filters can be designed programmatically. 
% In this case the function hpfilter was generated automatically from
% the Filter Design and Analysis Tool, but it could have just as well been
% created manually

% Design filter
fhp = hpfilter;

% "Decouple" acceleration due to body dynamics from gravity
ab = filter(fhp,acc);

% Compare the filtered signal with the original one
plotAccelerationColouredByActivity(t, [acc, ab], actid,...
    {'Original','High-pass filtered'})

%% Focus on a single activity first: select first portion of Walking signal
% Use logical indexing. In plain English, this is what we are trying to do:
% "Only select samples for which the activity was Walking and for which the
% time was less than 250 seconds"

% Assume we know the activity id for Walking is 1
walking = 1;
sel = (t < 250) & (actid == walking);

% Select only desired array segments for time vector
% and acceleration signal
tw = t(sel);
abw = ab(sel);

% Plot walking-only signal segment. Use interactive plot tools to zoom in
% and explore the signal. Note the quasi-periodic behavior.
figure
plotAccelerationColouredByActivity(tw, abw, [],'Walking')

%% Plot Power Spetral Density
% Use Welch method with its default options, using known sample frequency

% When called without output arguments, the function pwelch plots the PSD
figure
pwelch(abw,[],[],[],fs)

%% Validate potential of PSD to differentiate between different activities
% E.g. are position and height in the two respsctive sets of peaks
% different for different activities?

plotPSDActivityComparisonForSubject(1, 'Walking', 'WalkingUpstairs')

%% Validate consistency of PSD information across different subjects
% Compare Power Spectral Density of walking signals across all subjects in
% the dataset.

% This helper function uses a linear amplitude scale so PSD peaks
% visually stand out better
plotPSDForGivenActivity(walking)

%% Automate peak identification
% The function findpeaks in Signal Processing Toolbox can be used to
% identify amplitude and location of spectral peaks

% Compute numerical values of PSD and frequency vector. When called with
% one or two output arguments, the function pwelch does not automatically
% plot the PSD
[p,f] = pwelch(abw,[],[],[],fs);

% Use findpeaks to identify values (amplitude) and index locations of peaks
[pks,locs] = findpeaks(p);

% Plot PSD manually and overlay peaks
plot(f,db(p),'.-')
grid on
hold on
plot(f(locs),db(pks),'rs')
hold off
addActivityLegend(1)
title('Power Spectral Density with Peaks Estimates')
xlabel('Frequency (Hz)')
ylabel('Power/Frequency (dB/Hz)')

%% Refine peak finding by adding more specific requirements

% PSD with numerical output
[p,f] = pwelch(abw,[],[],[],fs);

% Find max 8 peaks, at least 0.25Hz apart from each other and with a given
% prominence value

fmindist = 0.25;                    % Minimum distance in Hz
N = 2*(length(f)-1);                % Number of FFT points
minpkdist = floor(fmindist/(fs/N)); % Minimum number of frequency bins

[pks,locs] = findpeaks(p,'npeaks',8,'minpeakdistance',minpkdist,...
    'minpeakprominence', 0.15);

% Plot PSD and overlay peaks
plot(f,db(p),'.-')
grid on
hold on
plot(f(locs),db(pks),'rs')
hold off
addActivityLegend(1)
title('Power Spectral Density with Peaks Estimates')
xlabel('Frequency (Hz)')
ylabel('Power/Frequency (dB/Hz)')


%% Autocorrelation as a feature
% Autocorrelation can also be powerful for frequency estimation.
% It is especially effective for estimating low-pitch fundamental
% frequencies

% xcorr with only one input will compute the autocorrelation 
[c, lags] = xcorr(abw);

% Highlight the main t=0 peak (overal energy) and a few secondary peaks
% The position of the second highest peaks identifies the main period
tmindist = 0.3;
minpkdist = floor(tmindist/(1/fs));
[pks,locs] = findpeaks(c,'minpeakprominence',1e4,...
    'minpeakdistance',minpkdist);

% Plot autocorrelation and three key peaks
tc = (1/fs)*lags;
plot(tc,c,'.-')
grid on
hold on
plot(tc(locs),c(locs),'rs')
hold off
xlim([-5,5])
addActivityLegend(1)
title('Autocorrrelation with Peaks Estimates')
xlabel('Time lag (s)')
ylabel('Correlation')

%% Check position of first peak varies between different activities
% Compare autocorrelation plots for same subject and different activity
% By zooming into the secong highest peaks, note how the respective
% second-peak positions are still spaced apart by more than a few samples.

plotCorrActivityComparisonForSubject(1, 'WalkingUpstairs', 'WalkingDownstairs')

%% Feature summary
% After exploring interactively a few different techniques to extract
% descriptive features from this type of signals, we can collect
% all the analysis methods identified into a single function.
% The responsibility of this function is to extract a fixed number
% of features for each signal buffer provided as input.

featureExtractionFcn = 'featuresFromBuffer';

edit(featureExtractionFcn)

%% Count number of actual code lines of function featuresFromBuffer.m
% Using MATLAB Central submission "sloc" by Raymond Norris, available at
% <http://www.mathworks.co.uk/matlabcentral/fileexchange/3900-sloc>

count = sloc(featureExtractionFcn);

fprintf('\n%d lines of source code found in %s.m\n', ...
    count, featureExtractionFcn);

%% Prepare data to train neural network
% To train the network, assume we:
% 
% * Re-organise the acceleration signals into shorter buffers of fixed
%   length L, each labeled with a single activity ID
% * Extract a vector of features for each Lx3 signal buffer [ax, ay, az]
%   using the function featuresFromBuffer 
% * Provide the network with two sets of feature vectors and corresponding
%   activity ID
% 
% The buffered data is already available and stored in
% the file BufferedAccelerations.mat
% 
% Computing the features is a fairly efficient process, but it takes a
% while in this case because of the high number fo signal vectors
% available.
% The pre-computed set of feature vectors for all available signal buffers
% is available in the file BufferFeatures.mat
% To re-compute all features use the function extractAllFeatures, which
% will
% 
% * Read the buffered signals from BufferedAccelerations.mat
% * Compute a feature vector for each buffer using featuresFromBuffer
% * Save all feature vectors into the file BufferFeatures.mat
% 
% extractAllFeatures can distribute the computations to a pool of workers
% if Parallel Computing Toolbox is installed
% 
% Now simply clear all variables that are not relevant anymore, and load
% pre-saved variables

% Clear nonrelevant variables
clear all %#ok<CLSCR>

% Load set of feature vectors (feat) and cell array of feature names
% (featlabels)
load('BufferFeatures.mat')

% Load buffered signals (here only using known activity IDs for buffers)
load('BufferedAccelerations.mat')

%% Train neural network for signal classification

% Reset random number generators
rng default

% Initialize a Neural Network with 18 nodes in hidden layer
% (assume the choice of the number 18 here is arbitrary)
net = patternnet(18);

% Organize features and known activity IDs so they can be consument by the
% train function
% NOTE: for real problems consider partitioning your dataset into training,
% validation and test subsets. This step has been left out here for
% simplicity.
X = feat';
tgtall = dummyvar(actid)';

% Train network
% For details about customizing the training function refer to the
% following:
% web(fullfile(docroot, 'nnet/ug/choose-a-multilayer-neural-network-training-function.html'))
net = train(net, X, tgtall);

%% Run Neural Network on buffered data
% We have now completed all the algorithmic steps necessary to implement
% the classification system presented at the very beginning of this
% example.
% 
% Opening the function runTrainedNetworkOnBufferedData will reveal the same
% code in this script section.
% 
% To use a pre-trained networ use (uncomment) the following line
% load('TrainedNetwork.mat')

% Re-initialize plot
clear plotAccelerationBufferAndPrediction

for k = 1:size(atx,1)
    % Get data - one buffer for each acceleration component
    ax = atx(k,:);
    ay = aty(k,:);
    az = atz(k,:);
    
    % Extract feature vector
    f = featuresFromBuffer(ax, ay, az, fs);
    
    % Classify with neural network
    scores = net(f');
    % Interpret result: use index of maximum score to retrieve the name of
    % the activity
    [~, maxidx] = max(scores);
    estimatedActivity = actnames{maxidx};
    actualActivity = actnames{actid(k)};

    % Plot three signals and display prediction result as title
    h = plotAccelerationBufferAndPrediction(ax,ay,az,t,...
        actualActivity,estimatedActivity);
    
    if ~ishandle(h)
        break
    end
end

%% Validate network more systematically, using a confusion matrix
% In the previous code cell we validated the predictive behavior of our
% trained neural network use a visual and qualitative approach.
% To quantitatively asses the performance of a classification algorithm one
% would normally measure the predictions over a whole test dataset, and
% compare them against the known class values.
% 
% The ultimate prediction performance can be represented visually in a
% number of different ways. Below we present the confusion matrix. The
% confusion matrix is a square matrix that summarizes the cumulative
% prediction results for all couplings between actual and predicted
% classes, respectively.
% 
% Normally it is good practice to use a test set different from the
% training set. This ensures that the results are not biased by the
% particular training dataset used.
%
% Even though we have ignored this principle so far, the Neural Network
% Toolbox includes the function dividerand, which automates most of
% the dataset partition mechanism.

% Randomly partition data between training, test and validation sets
[trainInd,valInd,testInd] = dividerand(size(X,2),0.7,0.15,0.15);
Xval = X(:,testInd);
yval = actid(testInd,:);
tgtval = dummyvar(yval)';

% Run network on validation set. This time predictions for all the
% different feature vectors are all produced and concatenated at once
scoreval = net(Xval);

% Display confusion matrix using prediction results
figure
plotconfusion(tgtval,scoreval)

