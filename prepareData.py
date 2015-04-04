def prepareData(bxtr, bytr, bztr,bxte,byte,bzte,subtr,ytr,subte,yte ):
    #made all the files arguments because your file path is different than mine and it makes loading the fiels easier
    import numpy
    ax_train = numpy.loadtxt(bxtr)
    ay_train = numpy.loadtxt(bytr)
    az_train = numpy.loadtxt(bztr)
    ax_test = numpy.loadtxt(bxte)
    ay_test = numpy.loadtxt(byte)
    az_test = numpy.loadtxt(bzte)

    atx=numpy.concatenate((ax_train,ax_test))
    aty=numpy.concatenate((ay_train,ay_test))
    atz=numpy.concatenate((az_train,az_test))

    s_train = numpy.loadtxt(subtr)
    y_train = numpy.loadtxt(ytr)
    s_test = numpy.loadtxt(subte)
    y_test = numpy.loadtxt(yte)

    subid = numpy.concatenate((s_train,s_test))
    actid = numpy.concatenate((y_train,y_test))

    actnames = {'Walking','WalkingUpstairs','WalkingDownstairs','Sitting','Standing','Laying'}

    fs = 50.0
    t = (1/fs) * atx.size
    
    filename = 'BufferedAccelerations'
    numpy.savez(filename,atx=atx,aty=aty,atz=atz,subid=subid,actid=actid,actnames=actnames,fs=fs,t=t)
 