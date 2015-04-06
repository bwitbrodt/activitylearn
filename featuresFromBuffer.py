def featuresFromBuffer(atx,aty,atz,fs):    
    import numpy
    #don't think we need to import all of scipy, uses memory as well
    #import scipy
    #from scipy import signal
    from scipy.signal import filter_design as fd
    from scipy.signal import lfilter
    from scipy.signal import iirfilter
    
    Fs = 50
    Ws = 0.4
    Wp = 0.8
    #As = 60
    As = 68.2282
    Rp = 1
    match = 'passband'
    #b,a = fd.iirdesign(Wp, Ws, Rp, As, btype = 'highpass',ftype='cheby2')
    b,a = iirfilter(7,0.016,rp = Rp,rs=As,btype='highpass',ftype='cheby2')
    
    #need to specify float variable otherwise defaults to an integer
    feat = numpy.zeros([1,66],float)

    abx = lfilter(b,a,atx)
    aby = lfilter(b,a,aty)
    abz = lfilter(b,a,atz)
    
    #this runs, but not sure if it is doign what we want
    #had to add the ":," in front of each feat[n], ex. feat[1] --> becomes feat [:,1]
    #because it was saying we didn't have the right dimintions
    #this "fixed it" but not 100% sure how 
    
    #video on multidimentional slicing
    #I think we should have a 1x66 array
    #https://training.enthought.com/course/NUMPY/lecture/MULTI_DIMENSIONAL_SLICING
    feat[:,0] = numpy.mean(abx)
    feat[:,1] = numpy.mean(aby)
    feat[:,2] = numpy.mean(abz)
    
    from numpy import mean, sqrt, square
    
    feat[:,3] = sqrt(mean(square(abx)))
    feat[:,4] = sqrt(mean(square(aby)))
    feat[:,5] = sqrt(mean(square(abz)))
    
    feat[:,6:8] = covFeatures(abx, fs)
    feat[:,9:11] = covFeatures(aby, fs)
    feat[:,12:14] = covFeatures(abz, fs)
    
    feat[:,15:26] = spectralPeaksFeatures(abx, fs)
    feat[:,27:38] = spectralPeaksFeatures(aby, fs)
    feat[:,39:50] = spectralPeaksFeatures(abz, fs)
    
    feat[:,51:55] = spectralPowerFeatures(abx, fs)
    feat[:,56:60] = spectralPowerFeatures(aby, fs)
    feat[:,61:65] = spectralPowerFeatures(abz, fs)
    
def covFeatures(x,fs):
    import numpy
    from scipy import signal #fftpack, ?? may need this see website: http://stackoverflow.com/questions/4688715/find-time-shift-between-two-similar-waveforms
    feats = numpy.zeros(3)
    c = numpy.correlate(x,x,"same")
    lags = numpy.argmax(signal.correlate(x,x))
    
    #lags = ?
    #I CANNOT FIGURE OUT HOW TO FIND "LAGS"
    #lags appears to be an argument 
    #http://www.mathworks.com/help/signal/ref/xcorr.html
    #example: [r,lags] = xcorr(___) also returns a vector with the lags at which the correlations are computed.
    
    ##from the matlab demo for this project
    ## Autocorrelation as a feature
    # Autocorrelation can also be powerful for frequency estimation.
    # It is especially effective for estimating low-pitch fundamental frequencies

    # xcorr with only one input will compute the autocorrelation 
    #[c, lags] = xcorr(abw);
    #according to matlab: lags is an output of the xcorr function, returning the "lag indices as a vector"

        
    minprom = 0.0005
    mindist_xunits = 0.3
    minpkdist = numpy.floor(mindist_xunits/(1/fs))

    from detect_peaks import detect_peaks
    locs = detect_peaks(c,threshold=minprom,mpd=minpkdist,show=True)
    pks = c[locs]
    #currently this finds zero peaks because minprom is too large. I left it because the filter is most likely wrong right now, resulting in wrong peak heights.

    tc = (1/fs)*lags
    tcl = tc(locs)
    tcl = (abs(tc))[locs]
    
    # Feature 0 - peak height at 0
    if tcl is not None:
        feats[0] = pks[(len(pks)+1)/2]

    # Features 1 and 2 - position and height of first peak 
    #if length(tcl) >= 3:
    if numpy.ndarray.size(tcl) >= 3:
        feats[1] = tcl[(len(pks)+1)/2+1]
        feats[2] = pks[(len(pks)+1)/2+1]
        
def spectralPeaksFeatures(x,fs):
    mindist_xunits = 0.3
    
    import numpy
    feats = numpy.zeros(12,float)
    
    N = 4096
    minpkdist = numpy.floor(mindist_xunits/(1/fs))
    
    import scipy
    from scipy import signal
    window = scipy.signal.get_window('boxcar',len(x))
    f,p = scipy.signal.welch(x,fs,window,noverlap='None',nfft=N)

    from detect_peaks import detect_peaks
    locs = detect_peaks(p,mpd=minpkdist,show=True)
    pks = p[locs]
    #Matlab only detects 20 peaks. No option in this code.
    
    if pks is not None:
        mx = min(6,len(pks))

        idx = sorted(range(len(pks)),key=lambda x:pks[x],reverse = True)
        spks = sorted(pks,reverse=True)
        
        slocs = locs[idx]
        
        pks = spks[0:mx]
        locs = slocs[0:mx]

        idx = sorted(range(len(locs)),key=lambda x:pks[x])
        slocs = sorted(slocs)        
        
        spks = pks[idx]
        pks = spks
        locs = slocs
    
    fpk = f[locs]

    feats[0:(len(pks)-1)] = fpk
    feats[6:(6+len(pks))] = pks

def spectralPowerFeatures(x,fs):
    import numpy
    feats = numpy.zeros(5)
    edges = [0.5,1.5,5,10,15,20]
    
    #import scipy
    from scipy import signal
    f,p = signal.scipy.periodogram(x,fs,window = None,nfft=4096)
    
    for kband in range(0,(len(edges)-2)):
        feats[kband] = sum(p[(f>=edges[kband]) and (f<edges[kband+1])])
    #something complex is going on here. I think I tracked it down at this link.
    #http://en.wikibooks.org/wiki/MATLAB_Programming/Print_Version
    #Look under "Logical Addressing"        
    # I think they are trying to sum all elements of P for which those two inequalities are true.

        