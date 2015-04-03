def prepareData():
    import numpy
    ax_train = numpy.loadtxt('C:/Users/gxen/Desktop/UCI HAR Dataset/UCI HAR Dataset/train/Inertial Signals/body_acc_x_train.txt')
    ay_train = numpy.loadtxt('C:/Users/gxen/Desktop/UCI HAR Dataset/UCI HAR Dataset/train/Inertial Signals/body_acc_y_train.txt')
    az_train = numpy.loadtxt('C:/Users/gxen/Desktop/UCI HAR Dataset/UCI HAR Dataset/train/Inertial Signals/body_acc_z_train.txt')
    ax_test = numpy.loadtxt('C:/Users/gxen/Desktop/UCI HAR Dataset/UCI HAR Dataset/test/Inertial Signals/body_acc_x_test.txt')
    ay_test = numpy.loadtxt('C:/Users/gxen/Desktop/UCI HAR Dataset/UCI HAR Dataset/test/Inertial Signals/body_acc_y_test.txt')
    az_test = numpy.loadtxt('C:/Users/gxen/Desktop/UCI HAR Dataset/UCI HAR Dataset/test/Inertial Signals/body_acc_z_test.txt')

    atx=numpy.concatenate((ax_train,ax_test))
    aty=numpy.concatenate((ay_train,ay_test))
    atz=numpy.concatenate((az_train,az_test))

    s_train = numpy.loadtxt('C:/Users/gxen/Desktop/UCI HAR Dataset/UCI HAR Dataset/train/subject_train.txt')
    y_train = numpy.loadtxt('C:/Users/gxen/Desktop/UCI HAR Dataset/UCI HAR Dataset/train/y_train.txt')
    s_test = numpy.loadtxt('C:/Users/gxen/Desktop/UCI HAR Dataset/UCI HAR Dataset/test/subject_test.txt')
    y_test = numpy.loadtxt('C:/Users/gxen/Desktop/UCI HAR Dataset/UCI HAR Dataset/test/y_test.txt')

    subid = numpy.concatenate((s_train,s_test))
    actid = numpy.concatenate((y_train,y_test))

    actnames = {'Walking','WalkingUpstairs','WalkingDownstairs','Sitting','Standing','Laying'}

    fs = 50.0
    t = (1/fs) * atx.size
    
    filename = 'BufferedAccelerations'
    numpy.savez(filename,atx=atx,aty=aty,atz=atz,subid=subid,actid=actid,actnames=actnames,fs=fs,t=t)
 