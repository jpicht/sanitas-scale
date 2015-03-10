#include "InterfaceClaim.h"

#include <usb.h>
#include <stdexcept>

namespace jpicht {
InterfaceClaim::InterfaceClaim(UsbDevice* usbDevice, int interface)
: dev(usbDevice->handle)
, claimedInterface(interface)
{
	if (0 != usb_claim_interface(dev, claimedInterface)) {
		throw std::runtime_error("Cannot claim device.");
	}
}

InterfaceClaim::~InterfaceClaim()
{
	usb_release_interface(dev, claimedInterface);
}
}
