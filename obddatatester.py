from  newobd import *
global com
#config here
osx= True
highseria=True
sleeptime=2


if osx:
    if highseria:
        com = OBDcom('/dev/tty.usbserial-00002014', 115200, '6')
    else:
        com = OBDcom('/dev/tty.usbserial-113010881974', 115200, '6')

else:
    com =OBDcom('/dev/ttyUSB0', 115200, '6')
if(debug):
    print('data: ' + str(com.query(commands.getPID("INTAKE_TEMP"))))


print('Setup Complete.')


#class for data storage
class datatype():

    def __init__(self, pid):
        self.PID = pid
        self.data=[]
    def update(self):
        temp = str(com.query(commands.getPID(self.PID)))
        self.data.append(temp)
        print('PID: '+self.PID+"     DATA: "+temp)
    def output(self):
        outstr=self.PID+'\n--------------\n'
        pt=0
        for s in self.data:
            outstr += str(pt*sleeptime)+' seconds'+': '+ self.data[pt]+'\n'


            pt=pt+1
        return outstr






#get data
data1=datatype('THROTTLE_POS')
data2=datatype('ENGINE_LOAD')
data3=datatype('COOLANT_TEMP')
data4=datatype('COOLANT_TEMP')
data5=datatype('COOLANT_TEMP')
dataarr =[data1,data2,data3,data4,data5]
def getdata():
    for d in dataarr:
        d.update()



print("GETTING RAW DATA")
print"RAW\n-----------------"

getdata()
time.sleep(sleeptime)
getdata()
time.sleep(sleeptime)
getdata()
time.sleep(sleeptime)
getdata()
time.sleep(sleeptime)
getdata()
time.sleep(sleeptime)
getdata()
time.sleep(sleeptime)




header='DATA FROM TEST ID 0001\n-----------------\n'



print (header)
print(data1.output())
print(data2.output())
print(data3.output())
print(data4.output())
print(data5.output())
print('record data to file?(y/n)')
yn = raw_input("Y/N:")
if yn.capitalize()=="Y":
    yn=True
else:
    yn=False

if yn:
    print ("write to file")
    file = open('testdata.txt', 'a')
    file.write('\n\n\n*****************\n')
    for a in dataarr:
        file.write(a.output()+"\n")
    file.flush()
    file.close()
    print('done')
else:
    print('Skip file write')

