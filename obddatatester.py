from  newobd import *
global com
osx= True
if osx:
    com = OBDcom('/dev/tty.usbserial-113010881974', 115200, '6')
else:
    com =OBDcom('/dev/ttyUSB0', 115200, '6')
if(debug):
    print('data: ' + str(com.query(commands.getPID("INTAKE_TEMP"))))


print('Setup Complete.')
#get data
def prindata():
    data1='THROTTLE_POS'
    data2='ENGINE_LOAD'
    data3='COOLANT_TEMP'
    data4='COOLANT_TEMP'
    data5='COOLANT_TEMP'

    print(data1+": "+ str(com.query(commands.getPID(data1))))
    print(data2+": "+ str(com.query(commands.getPID(data2))))
    print(data3+": "+ str(com.query(commands.getPID(data3))))
    print(data4+": "+ str(com.query(commands.getPID(data4))))
    print(data5+": "+ str(com.query(commands.getPID(data5))))

prindata()
time.sleep(2)
prindata()
time.sleep(2)
prindata()
time.sleep(2)
prindata()
time.sleep(2)
prindata()
time.sleep(2)
