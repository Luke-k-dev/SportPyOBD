import pandas as pd
import os, sys
class Recorder():
    def __init__(self):
        self.PIDS= []
        self.Recording= False
        self.Time=1
        fileext='.xls'
        filepath='/DATA_RECORDINGS/'
        #get path
        print 'sys.argv[0] =', sys.argv[0]
        pathname = os.path.dirname(sys.argv[0])
        print 'path =', pathname
        fullpath=os.path.abspath(pathname)+filepath
        print 'full path =', fullpath
        #check to how many files there are
        filearr=os.listdir(fullpath)
        print(len(filearr))
        self.filenameandpath= fullpath+'DATA_LOG_'+str(len(filearr))+fileext
        print(self.filenameandpath)


    def SetPIDS(self, pidarr):
        self.PIDS= pidarr
    def GenFrame(self):
        self.DATAFRAME = pd.DataFrame(columns=self.PIDS)

    ###Data methods here
    def WriteToFile(self):
        writer = pd.ExcelWriter(self.filenameandpath, engine='xlsxwriter')

        print (self.DATAFRAME)
        self.DATAFRAME.to_excel(writer, 'Sheet1')

    def AdvanceTime(self):
        self.Time+=1

    def recordTimeSlot(self, PID, value):
        #we look through matrix and find first value in time colum that is empty then assign to that column
        #self.DATAFRAME.set_value(time, PID,value)
        self.DATAFRAME.at[self.Time, PID]=value
'''d = Recorder()
pidar=['FUEL','RPM','BOOST','OIL TEMP', 'COOLANT TEMP']
d.SetPIDS(pidar)
d.GenFrame()
#print(d.GETTABLESTRING())
d.recordTimeSlot(1, 'FUEL',55)
d.recordTimeSlot(2, 'FUEL',55)
d.recordTimeSlot(3, 'FUEL',55)
d.recordTimeSlot(4, 'FUEL',55)
d.recordTimeSlot(5, 'FUEL',51)

d.WriteToFile()'''

