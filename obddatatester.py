from  newobd import *
global com
#config here
osx= True
highseria=True
sleeptime=1


if osx:
    if highseria:
        com = OBDcom('/dev/tty.usbserial-00002014', 115200, '6')
    else:
        com = OBDcom('/dev/tty.usbserial-113010881974', 115200, '6')

else:
    com =OBDcom('/dev/ttyUSB0', 115200, '6')

print('Setup Complete.')

#class for data storage
class datatype():

    def __init__(self, pid):
        self.PID = pid
        self.data=[]
        print("registered :"+self.PID)
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
data4=datatype('FRS_OIL_TEMP')
data5=datatype('VIN')
dataarr =[data1,data2,data3,data4,data5]
dataarr=[data5]

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
key='DATA KEY\n-------------\n'
for k in dataarr:
    d=''
    d=d+str(commands.getPID(k.PID).getDescription())
    print(d)
    pi =str(k.PID)
    key+= pi +": " + d +"\n"


print (header)
print(key)
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
    file.write('\n******NEW TEST HERE*******\n')
    file.write(key)
    for a in dataarr:
        file.write(a.output()+"\n")
    print('data in buffer preparing to flush')
    file.flush()
    print('data has been flushed')
    file.close()
    print('done')
else:
    print('Skip file write')



