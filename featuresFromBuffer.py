def featuresFromBuffer(atx,aty,atz,fs):    
    import numpy
    import scipy
    from scipy import signal
    from scipy.signal import filter_design as fd
    from scipy.signal import lfilter
    
    Fs = 50
    Ws = 0.4
    Wp = 0.8
    As = 60
    Rp = 1
    match = 'passband'
    b,a = fd.iirdesign(Wp, Ws, Rp, As, ftype='ellip')
    
    feat = numpy.zeros(66)
    
    abx = lfilter(b,a,atx)
    aby = lfilter(b,a,aty)
    abz = lfilter(b,a,atz)
    
    feat[0] = numpy.mean(abx)
    feat[1] = numpy.mean(aby)
    feat[2] = numpy.mean(abz)
    
    from numpy import mean, sqrt, square
    
    feat[3] = sqrt(mean(square(abx)))
    feat[4] = sqrt(mean(square(aby)))
    feat[5] = sqrt(mean(square(abz)))
    
    feat[6:8] = covFeatures(abx, fs)
    feat[9:11] = covFeatures(aby, fs)
    feat[12:14] = covFeatures(abz, fs)
    
    feat[15:26] = spectralPeaksFeatures(abx, fs)
    feat[27:38] = spectralPeaksFeatures(aby, fs)
    feat[39:50] = spectralPeaksFeatures(abz, fs)
    
    feat[51:55] = spectralPowerFeatures(abx, fs)
    feat[56:60] = spectralPowerFeatures(aby, fs)
    feat[61:65] = spectralPowerFeatures(abz, fs)
    
def covFeatures(x,fs):
    import numpy
    feats = numpy.zeros(3)
    c = numpy.correlate(x,x,"same")
    #lags = ?
    #I CANNOT FIGURE OUT HOW TO FIND "LAGS"
        
    minprom = 0.0005
    mindist_xunits = 0.3
    minpkdist = numpy.floor(mindist_xunits/(1/fs))

    from detect_peaks import detect_peaks
    locs = detect_peaks(c,threshold=minprom,mpd=minpkdist)#,show=True)
    pks = c[locs]
    #currently this finds zero peaks because minprom is too large. I left it because the filter is most likely wrong right now, resulting in wrong peak heights.

    tc = (1/fs)*lags
    tcl = tc(locs);
    
    # Feature 0 - peak height at 0
    if tcl is not None:
        feats[0] = pks[(len(pks)+1)/2]

    # Features 1 and 2 - position and height of first peak 
    if length(tcl) >= 3:
        feats[1] = tcl[(len(pks)+1)/2+1]
        feats[2] = pks[(len(pks)+1)/2+1]
        
def spectralPeaksFeatures(x,fs):
    mindist_xunits = 0.3
    
    import numpy
    feats = numpy.zeros(12)
    
    N = 4096
    minpkdist = numpy.floor(mindist_xunits/(1/fs))
    
    import scipy
    from scipy import signal
    window = scipy.signal.get_window('boxcar',len(x))
    f,p = scipy.signal.welch(x,fs,window,noverlap='None',nfft=N)

    from detect_peaks import detect_peaks
    locs = detect_peaks(p,mpd=minpkdist)#,show=True)
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
    
    import scipy
    from scipy import signal
    f,p = signal.scipy.periodogram(x,fs,window = None,nfft=4096)
    
    for kband in range(0,(len(edges)-2)):
        feats[kband] = sum(p[(f>=edges[kband]) and (f<edges[kband+1])])
    #something complex is going on here. I think I tracked it down at this link.
    #http://en.wikibooks.org/wiki/MATLAB_Programming/Print_Version
    #Look under "Logical Addressing"        
    # I think they are trying to sum all elements of P for which those two inequalities are true.

        