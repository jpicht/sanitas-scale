#include "UsbDevice.h"

#include <usb.h>
#include <stdexcept>

namespace jpicht {
UsbDevicePtr UsbDevice::findDevice(UsbScope &scope, unsigned int vendorId, unsigned int productId)
{
	struct usb_bus *usbBus;
	struct usb_device *device;
	usb_dev_handle *handle = 0;

	usb_find_busses();
	usb_find_devices();

	usbBus = usb_busses;
	while(usbBus)
	{
		device = usbBus->devices;
		while(device)
		{
			if(vendorId  == device->descriptor.idVendor
			&& productId == device->descriptor.idProduct)
			{
				handle = usb_open(device);
				return UsbDevicePtr(new UsbDevice(handle));
			}
			device = device->next;
		}
		usbBus = usbBus->next;
	}

	throw std::runtime_error("Cannot find device.");
}

void UsbDevice::claimInterface(int interface)
{
	if (0 != usb_claim_interface(handle, 0)) {
		throw std::runtime_error("Cannot claim device.");
	}
}

int UsbDevice::controlMsg(unsigned char request, unsigned char rType, unsigned int value, unsigned int index, char* buffer, ssize_t size, int timeout)
{
	return usb_control_msg(handle, request, rType, value, index, buffer, size, timeout);
}

bool UsbDevice::interruptRead(int endpoint, std::vector<unsigned char> &buffer, size_t length, int timeout)
{
	std::auto_ptr<char> localBuffer(new char(length));
	int actuallyRead = usb_interrupt_read(handle, endpoint, localBuffer.get(), length, timeout);

	if (actuallyRead == length) {
		for (int i = 0; i < length; ++i) {
			buffer.push_back(localBuffer.get()[i]);
		}
		return true;
	}

	return false;
}

}

