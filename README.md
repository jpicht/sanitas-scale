scale
=====
This tool implements a very rudementary interface to the "Sanitas SBF-48 Diagnostic scale". Currently the only function is to dump the memory contents of the scale to a binary dump file.

System Requirements
-------------------
The software is only tested on my Ubuntu 14.04 system. It needs the package ```libusb-dev``` to be installed to compile it.

You need to detach the standard usbhid driver from the device, then disconnect and reconnect it.

```
sudo -i
rmmod usbhid; modprobe usbhid quirks=0x04d9:0x8010:0x0004
```

Notice that both commands are on the same line. I have to do it like that, because if I only removed the usbhid driver, my keyboard would not be usable anymore.

The tool needs access to the usb device, so either you need to change the device file, to be writeable by your user or simply run the tool as the root user.

Compile and run
---------------
To compile the program simply run ```make```.

To run it:
```
sudo ./scale outputfile.bin
```

Links
-----
- http://www.sanitas-online.de/web/de/produkte/gewicht/SBF48.php
- http://www.sanitas-online.de/web/_dokumente/GAs/gewicht/750.882-0313_SBF48.pdf
