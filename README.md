# SCPI-Lite
Light-weight SCPI library for easy scripting access to instruments

This library abstracts the underlying transport between computer and the instrument.
Goal is to allow easy "scripting" withouth having to worry about the physical transport.
And being able to talk to any device implementing SCPI (or "SCPI like") protocol, withouth
having to have device / dialect specific driver.

Currently supported transports (backends) are:
* Serial 
* TCP/IP
* Linux USBTMC (/dev/usbtmc*)
* USBTMC (direct USB access)

## Requirements

Library has been written on Python 3.x. It uses following Python modules:
* serial (pySerial)
* usbtmc - needed for direct USB access (not needed if using Linux USBTMC)

## Usage

This module provides _SCPIDevice_ class that represents connection to instrument.

Device string parameter is used to automaticallyd determine underlying transport
to use:

Transport|Example|Notes
---|----|----
USBTMC|USB::0x1ab1::0x0e11::INSTR|Connect to USBTMC device using usbtmc module
Linux USBTMC|/dev/usbtmc0|Connect to USBTMC device using Linux kernel module
TCP|192.168.42.42:5555|Connect to device using TCP/IP
Serial|/dev/ttyS0, /dev/ttyUSB0, or COM1: (Windows)|This is the default method if devices string doesnt match to any known format


Connection examples:

```
dev = scpi_lite.SCPIDevice('/dev/usbtmc0')
```

```
dev = scpi_lite.SCPIDevice('/dev/ttyUSB0', baudrate=115200, timeout=5)
```

```
dev = scpi_lite.SCPIDevice('192.168.42.42:5555', timeout=5)
```

### Generic options for SCPIDevice class

Following options are supported by the _SCPIDevice_ class currently:

Option|Description|Example
------|-----------|-------
idn|Device supports *IDN? command (boolean) [Default: True]|idn=False
opc|Device supports *OPC? command (boolean) [Default: True]|opc=False
err|Device supports SYST:ERR? command (boolean) [Default: True]|err=False
command_terminator|Command terminator (allows overriding SCPI default in case of non-compliant device) [Default: \n]|command_terminator=''
encoding|Command (string) encoding [Default: utf-8]|

### Transport specific options for SCPIDevice class

There are transport specific options that can be passed throug as well:

Transport|Option|Description|Example
---------|------|-----------|-------
*all*|timeout|Timeout for waiting response from the instrument (in seconds) [Default: 5]|timeout=10
*all*|verbose|Enable verbose/debug output (boolean) [Default: False]|verbose=True
serial|baudrate|Baud rate (bps) [Default: 115200]|baudrate=9600
serial|bytesize|Byte size [Default: EIGHTBITS]|bytesize=serial.SEVENBITS
serial|parity|Parity [Default: PARITY_NONE]|parity=serial.PARITY_EVEN
serial|stopbits|Stop bits [Default: STOPBITS_ONE]|stopbits=serial.STOPBITS_TWO
serial|xonxoff|Use XON/XOFF flow-controll [Default: Flase]|xonxoff=True
serial|rtscts|Use RTS/CTS flow-control [Default: False]|rtscts=True
serial|dsrdtr|Use DSR/DTR flow-control [Default: False]|dsrdtr=True
  
  
## Examples


```
import scpi_lite

print('scpi_lite version: ',scpi_lite.VERSION)


# connect to instrument

#dev = scpi_lite.SCPIDevice('USB::0x1ab1::0x0e11::INSTR')
#dev = scpi_lite.SCPIDevice('/dev/usbtmc0')
dev = scpi_lite.SCPIDevice('192.168.42.42:5555')

# enable debug output
dev.verbose=1

# display instrument model and firmware version
print('Instrument: %s v%s' % (dmm.model, dmm.firmware))

# send a 'query' to instrument
val = dev.query('SYST:VERS?')
print('response: ', val)

# if there was error running query error can be checked using last_error variable
print('result: ', psu.last_error)


# send a command to instrument
res = dev.command('SYST:REM')

# check if command was successfull
print('result', res)

```




