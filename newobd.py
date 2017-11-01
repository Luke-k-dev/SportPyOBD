
#from OBDSIM import *
from os import system
#global vars here
#---------------------
loopct = 0
speed =0
rpm =0
oiltemp = 0
intakepressue =0
hascar = True
osx= True #change to false on linux
debug = False
import re
import serial
import time

from protocols import *

class OBDcom:
    _SUPPORTED_PROTOCOLS = {
        #"0" : None, # Automatic Mode. This isn't an actual protocol. If the
                     # ELM reports this, then we don't have enough
                     # information. see auto_protocol()
        "1" : SAE_J1850_PWM,
        "2" : SAE_J1850_VPW,
        "3" : ISO_9141_2,
        "4" : ISO_14230_4_5baud,
        "5" : ISO_14230_4_fast,
        "6" : ISO_15765_4_11bit_500k,
        "7" : ISO_15765_4_29bit_500k,
        "8" : ISO_15765_4_11bit_250k,
        "9" : ISO_15765_4_29bit_250k,
        "A" : SAE_J1939,
        #"B" : None, # user defined 1
        #"C" : None, # user defined 2
    }

    # used as a fallback, when ATSP0 doesn't cut it
    _TRY_PROTOCOL_ORDER = [
        "6", # ISO_15765_4_11bit_500k
        "8", # ISO_15765_4_11bit_250k
        "1", # SAE_J1850_PWM
        "7", # ISO_15765_4_29bit_500k
        "9", # ISO_15765_4_29bit_250k
        "2", # SAE_J1850_VPW
        "3", # ISO_9141_2
        "4", # ISO_14230_4_5baud
        "5", # ISO_14230_4_fast
        "A", # SAE_J1939
    ]
    
    ELM_PROMPT = b'>'
    def __init__(self, portname, baudrate, protocol):
        """Initializes port by resetting device and gettings supported PIDs. """

        print("Initializing ELM327: PORT=%s BAUD=%s PROTOCOL=%s" %
                    (
                        portname,
                        "auto" if baudrate is None else baudrate,
                        "auto" if protocol is None else protocol,
                    ))
        


        # ------------- open port -------------
        try:
            self.__port = serial.Serial(portname, \
                                        parity   = serial.PARITY_NONE, \
                                        stopbits = 1, \
                                        bytesize = 8,
                                        timeout = 10) # seconds
        except serial.SerialException as e:
            print(e)
            return
        except OSError as e:
            print(e)
            return

        # ------------------------ find the ELM's baud ------------------------

        if not self.set_baudrate(baudrate):
            self.__error("Failed to set baudrate")
            return

        # ---------------------------- ATZ (reset) ----------------------------
        try:
            self.__send(b"ATZ", delay=1) # wait 1 second for ELM to initialize
            # return data can be junk, so don't bother checking
        except serial.SerialException as e:
            self.__error(e)
            return

        # -------------------------- ATE0 (echo OFF) --------------------------
        r = self.__send(b"ATE0")
        

        # ------------------------- ATH1 (headers ON) -------------------------
        r = self.__send(b"ATH1")
        

        # ------------------------ ATL0 (linefeeds OFF) -----------------------
        r = self.__send(b"ATL0")
       
        # by now, we've successfuly communicated with the ELM, but not the car
       
        # try to communicate with the car, and load the correct protocol parser
        if self.set_protocol( protocol):
            print("Connected Successfully: PORT=%s BAUD=%s PROTOCOL=%s" %
                        (
                            portname,
                            self.__port.baudrate,
                            self.__protocol.ELM_ID,
                        ))
        else:
            print("Connected to the adapter, but failed to connect to the vehicle")

    def set_protocol(self, protocol):
        if protocol is not None:
            # an explicit protocol was specified
            if protocol not in self._SUPPORTED_PROTOCOLS:
                print("%s is not a valid protocol. Please use \"1\" through \"A\"")
                return False
            return self.manual_protocol(protocol)
        else:
            # auto detect the protocol
            return self.auto_protocol()
        
    def manual_protocol(self, protocol):
        r = self.__send(b"ATTP" + protocol.encode())
        r0100 = self.__send(b"0100")

        if not self.__has_message(r0100, "UNABLE TO CONNECT"):
            # success, found the protocol
            self.__protocol = self._SUPPORTED_PROTOCOLS[protocol](r0100)
            return True

        return False

    def auto_protocol(self):
        """
            Attempts communication with the car.

            If no protocol is specified, then protocols at tried with `ATTP`

            Upon success, the appropriate protocol parser is loaded,
            and this function returns True
        """

        # -------------- try the ELM's auto protocol mode --------------
        r = self.__send(b"ATSP0")

        # -------------- 0100 (first command, SEARCH protocols) --------------
        r0100 = self.__send(b"0100")

        # ------------------- ATDPN (list protocol number) -------------------
        r = self.__send(b"ATDPN")
        if len(r) != 1:
            print("Failed to retrieve current protocol")
            return False


        p = r[0] # grab the first (and only) line returned
        # suppress any "automatic" prefix
        p = p[1:] if (len(p) > 1 and p.startswith("A")) else p

        # check if the protocol is something we know
        if p in self._SUPPORTED_PROTOCOLS:
            # jackpot, instantiate the corresponding protocol handler
            self.__protocol = self._SUPPORTED_PROTOCOLS[p](r0100)
            return True
        else:
            # an unknown protocol
            # this is likely because not all adapter/car combinations work
            # in "auto" mode. Some respond to ATDPN responded with "0"
            print("ELM responded with unknown protocol. Trying them one-by-one")

            for p in self._TRY_PROTOCOL_ORDER:
                r = self.__send(b"ATTP" + p.encode())
                r0100 = self.__send(b"0100")
                if not self.__has_message(r0100, "UNABLE TO CONNECT"):
                    # success, found the protocol
                    self.__protocol = self._SUPPORTED_PROTOCOLS[p](r0100)
                    return True

        # if we've come this far, then we have failed...
        print("Failed to determine protocol")
        return False


    def set_baudrate(self, baud):
        if baud is None:
            # when connecting to pseudo terminal, don't bother with auto baud
            if self.port_name().startswith("/dev/pts"):
                print("Detected pseudo terminal, skipping baudrate setup")
                return True
            else:
                return self.auto_baudrate()
        else:
            self.__port.baudrate = baud
            return True

    def __has_message(self, lines, text):
        for line in lines:
            if text in line:
                return True
        return False
    
    def __send(self, cmd, delay=.3):
        """
            unprotected send() function

            will __write() the given string, no questions asked.
            returns result of __read() (a list of line strings)
            after an optional delay.
        """

        self.__write(cmd)

        if delay is not None:
            print("wait: %d seconds" % delay)
            time.sleep(delay)

        return self.__read()


    def __write(self, cmd):
        """
            "low-level" function to write a string to the port
        """

        if self.__port:
            cmd += b"\r\n" # terminate
            print("write: " + repr(cmd))
            self.__port.flushInput() # dump everything in the input buffer
            self.__port.write(cmd) # turn the string into bytes and write
            self.__port.flush() # wait for the output buffer to finish transmitting
        else:
            print("cannot perform __write() when unconnected")

    def send_and_parse(self, cmd):
        """
            send() function used to service all OBDCommands

            Sends the given command string, and parses the
            response lines with the protocol object.

            An empty command string will re-trigger the previous command

            Returns a list of Message objects
        """

        lines = self.__send(cmd)
        messages = self.__protocol(lines)
        return messages
    
    def __read(self):
        """
            "low-level" read function

            accumulates characters until the prompt character is seen
            returns a list of [/r/n] delimited strings
        """
        if not self.__port:
            print("cannot perform __read() when unconnected")
            return []

        buffer = bytearray()

        while True:
            # retrieve as much data as possible
            data = self.__port.read()

            # if nothing was recieved
            if not data:
                print("Failed to read port")
                break

            buffer.extend(data)

            # end on chevron (ELM prompt character)
            if self.ELM_PROMPT in buffer:
                break

        # log, and remove the "bytearray(   ...   )" part
        print("read: " + repr(buffer)[10:-1])

        # clean out any null characters
        buffer = re.sub(b"\x00", b"", buffer)

        # remove the prompt character
        if buffer.endswith(self.ELM_PROMPT):
            buffer = buffer[:-1]

        # convert bytes into a standard string
        string = buffer.decode()

        # splits into lines while removing empty lines and trailing spaces
        lines = [ s.strip() for s in re.split("[\r\n]", string) if bool(s) ]

        return lines
#only one usbcom device allowed with this program
if osx:
    com = OBDcom('/dev/tty.usbserial-113010881974', 115200, '1')
else:
    com =OBDcom('/dev/ttyUSB0', 115200, None)
if(debug):
    ans = com.send_and_parse(b'0101')
    print(ans[0].raw())
    ans = com.send_and_parse(b'0100')
    print(ans[0].raw())
    ans = com.send_and_parse(b'010c')
    print(ans[0].raw())


print('Setup Complete.')
