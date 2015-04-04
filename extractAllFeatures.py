def extractAllFeatures():
    import numpy

    s = numpy.load('BufferedAccelerations.npz')
    #infor for how to read data from a .npz file
    #http://stackoverflow.com/questions/17912878/unable-to-load-non-arrays-from-an-npz-file
    
    newf = numpy.zeros(66 - len(s['atx']) + 1)
    
    tic()
    
    import featuresFromBuffer
    for n in range(0,len(s['atx'])):
        #again need to use s['asx'], ect. to get variables right
        newf[n,:] = featuresFromBuffer(s['atx'][n,:],s['aty'][n,:],s['atz'][n,:],s['fs'][n,:])
    
    toc()
    
    x = newf
    feat = x
    featlabels = getFeatureNames()
    
    filename = 'BufferFeaturesNew'
    numpy.savez(filename,feat=feat,featlabels=featlabels)
 
def getFeatureNames():
    import numpy
    featureNames = numpy.zeros((66,2))
    featureNames[0,0] = {'TotalAccXMean'};
    featureNames[1,0] = {'TotalAccYMean'};
    featureNames[2,0] = {'TotalAccZMean'};
    featureNames[3,0] = {'BodyAccXRMS'};
    featureNames[4,0] = {'BodyAccYRMS'};
    featureNames[5,0] = {'BodyAccZRMS'};
    featureNames[6,0] = {'BodyAccXCovZeroValue'};
    featureNames[7,0] = {'BodyAccXCovFirstPos'};
    featureNames[8,0] = {'BodyAccXCovFirstValue'};
    featureNames[9,0] = {'BodyAccYCovZeroValue'};
    featureNames[10,0] = {'BodyAccYCovFirstPos'};
    featureNames[11,0] = {'BodyAccYCovFirstValue'};
    featureNames[12,0] = {'BodyAccZCovZeroValue'};
    featureNames[13,0] = {'BodyAccZCovFirstPos'};
    featureNames[14,0] = {'BodyAccZCovFirstValue'};
    featureNames[15,0] = {'BodyAccXSpectPos1'};
    featureNames[16,0] = {'BodyAccXSpectPos2'};
    featureNames[17,0] = {'BodyAccXSpectPos3'};
    featureNames[18,0] = {'BodyAccXSpectPos4'};
    featureNames[19,0] = {'BodyAccXSpectPos5'};
    featureNames[20,0] = {'BodyAccXSpectPos6'};
    featureNames[21,0] = {'BodyAccXSpectVal1'};
    featureNames[22,0] = {'BodyAccXSpectVal2'};
    featureNames[23,0] = {'BodyAccXSpectVal3'};
    featureNames[24,0] = {'BodyAccXSpectVal4'};
    featureNames[25,0] = {'BodyAccXSpectVal5'};
    featureNames[26,0] = {'BodyAccXSpectVal6'};
    featureNames[27,0] = {'BodyAccYSpectPos1'};
    featureNames[28,0] = {'BodyAccYSpectPos2'};
    featureNames[29,0] = {'BodyAccYSpectPos3'};
    featureNames[30,0] = {'BodyAccYSpectPos4'};
    featureNames[31,0] = {'BodyAccYSpectPos5'};
    featureNames[32,0] = {'BodyAccYSpectPos6'};
    featureNames[33,0] = {'BodyAccYSpectVal1'};
    featureNames[34,0] = {'BodyAccYSpectVal2'};
    featureNames[35,0] = {'BodyAccYSpectVal3'};
    featureNames[36,0] = {'BodyAccYSpectVal4'};
    featureNames[37,0] = {'BodyAccYSpectVal5'};
    featureNames[38,0] = {'BodyAccYSpectVal6'};
    featureNames[39,0] = {'BodyAccZSpectPos1'};
    featureNames[40,0] = {'BodyAccZSpectPos2'};
    featureNames[41,0] = {'BodyAccZSpectPos3'};
    featureNames[42,0] = {'BodyAccZSpectPos4'};
    featureNames[43,0] = {'BodyAccZSpectPos5'};
    featureNames[44,0] = {'BodyAccZSpectPos6'};
    featureNames[45,0] = {'BodyAccZSpectVal1'};
    featureNames[46,0] = {'BodyAccZSpectVal2'};
    featureNames[47,0] = {'BodyAccZSpectVal3'};
    featureNames[48,0] = {'BodyAccZSpectVal4'};
    featureNames[49,0] = {'BodyAccZSpectVal5'};
    featureNames[50,0] = {'BodyAccZSpectVal6'};
    featureNames[51,0] = {'BodyAccXPowerBand1'};
    featureNames[52,0] = {'BodyAccXPowerBand2'};
    featureNames[53,0] = {'BodyAccXPowerBand3'};
    featureNames[54,0] = {'BodyAccXPowerBand4'};
    featureNames[55,0] = {'BodyAccXPowerBand5'};
    featureNames[56,0] = {'BodyAccYPowerBand1'};
    featureNames[57,0] = {'BodyAccYPowerBand2'};
    featureNames[58,0] = {'BodyAccYPowerBand3'};
    featureNames[59,0] = {'BodyAccYPowerBand4'};
    featureNames[60,0] = {'BodyAccYPowerBand5'};
    featureNames[61,0] = {'BodyAccZPowerBand1'};
    featureNames[62,0] = {'BodyAccZPowerBand2'};
    featureNames[63,0] = {'BodyAccZPowerBand3'};
    featureNames[64,0] = {'BodyAccZPowerBand4'};
    featureNames[65,0] = {'BodyAccZPowerBand5'};
    
    
def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print "Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds."
    else:
        print "Toc: start time not set"