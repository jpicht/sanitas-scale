#include "Scale.h"

#include <stdexcept>
#include <iostream>

namespace jpicht {
Scale::Scale(UsbDevicePtr scaleDevice_)
: scaleDevice(scaleDevice_)
, claim(scaleDevice.get(), 0)
{
	std::auto_ptr<char> buffer(new char[8]);
	buffer.get()[0] = 0x10;

	if (0 != scaleDevice->controlMsg(0x21, 0x0a, 0x0000, 0, 0, 0, 1000)) {
		throw std::runtime_error("Got unexpected result code for first control message.");
	}
	if (8 != scaleDevice->controlMsg(0x21, 0x09, 0x0300, 0, (char*) buffer.get(), 8, 1000)) {
		throw std::runtime_error("Got unexpected result code for second control message.");
	}

	while (scaleDevice->interruptRead(1, output, 8, 1000));
}

ScalePtr Scale::findScale(UsbScope &scope)
{
	return ScalePtr(new Scale(UsbDevice::findDevice(scope, Scale::USB_VENDOR_ID, Scale::USB_PRODUCT_ID)));
}

std::ostream &operator<<(std::ostream &output, const Scale &S)
{
	std::cerr << "Size: " << S.output.size() << std::endl;
	for (int i = 0; i < S.output.size(); ++i) {
		output << S.output[i];
	}
}

}
