# SportPyOBD
Initially this was to be a package to easily create OBDII interfaces, however over its development I have instead created an OBDII interface program. It is designed to run on OSX and the respberrypi. It has a clean modern UI that is easily editable, and can record vehicle data.

<h2>Acknowledgements</h2>
<p>As with many works, this is one built off of fantastic work by others. I have built this software using some coede from https://github.com/brendan-w who used code from https://github.com/peterh/pyobd. My goal in this project is to update their work to make it work easily with the FRS/BRZ/86 and provide an easy to customize graphical interface for the data. I am also open to supporting more cars but as of now, this project will be directed tword the car models listed above.</p>

<h1>Prereqs</h1>
<ul>
  <li>Python 2.7</li>
  <li>Pyserial from <code>sudo pip install serial</code></li>
  <li>obd from <code>sudo pip install obd</code></li>
  <li>This package properly installed</li>
  <li>OBD2 ELM 327 USB adapter</li>
  <li>HDMI Display</li>
  <li>ELM 327 COM Port Driver (Should come with adapter or be installed with linux)</li>
  <li>Screen (sudo apt-get install screen) this is for testing car commands and to verify setup</li>
</ul>
<br>

<h1>Check to see if your connection is good.</h1>
<p>use this command on linux once you have installed screen. <code>screen /dev/ttyUSB0 [baudrateofelmdevice]</code><br>
  Next clear the connection with <code>atz</code><br>
  Next test the connection with <code>0100</code><br>
  The return on these codes will be hex(computer giberish), as long as you dont get an error you are good.<br>
  <b>NOTE: THESE ARE HEX COMMANDS SENT TO YOUR CAR, ONLY USE CODES STARTING WITH '01' other codes can damage your ECU. I am not liable for any ECU damage for any reason.</b>
  Also I will note here that some ELM327 adapters drain car power even when turned off, so be mindful of this when leaving your car unatended for long portions of time.
</p>

<h1>Usage</h1>
<p>Initially this was to be a package to easily create OBDII interfaces, however over its development I have instead created an OBDII interface program. It is designed to run on OSX and the respberrypi. To use simply download the package, make sure you have the OBDII drivers installed, make sure the port is correct in the newOBD class(/dev/ttyUSB0/ or something), connect to your car, and run main.py
  <b>NOTE: YOU MUST SET UIINDEBUG =  False in Main.py IF YOU DO NOT DO THIS SportPyOBD will not connect</b>
</p>


<h1>Help! How do I code the GUI?!</h1>
<p>Relax, this project uses tkinter. It is installed with practically every python instalation and is very simple. More info on tkinter here: https://wiki.python.org/moin/TkInter.</p>
<br>
<p>Each gui componet is orginized into one 'block' of code, each block has a comment above it stating its function. Each parameter references either the ColorPallet class or the css class. This is desgined so that the program may have easily changable style. Please checkout each class before making changes to GUI parameters.</p>


<h1>Common Problems</h1>
<ul>
  <li>Getting NO DATA back from car <b>FIX: Check your init code parameters. make sure you pass the right port arg AND baud rate to the OBD class</b></li>
  <li>OBD connection errors <b>FIX: The OBD port is fussy, unplug the adapter and then plug it back in making sure it is fully inserted.</b></li>
  <li>Feel free to open an issue if you find something wrong.</li>
</ul>
<br>


