#pragma once

#include <usb.h>
#include "UsbDevice.h"

namespace jpicht
{
	class InterfaceClaim
	{
	public:
		InterfaceClaim(UsbDevice* usbDevice, int interface);
		~InterfaceClaim();

		usb_dev_handle *dev;
		int claimedInterface;
	};
}

