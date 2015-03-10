#pragma once

#include "UsbDevice.h"
#include "InterfaceClaim.h"

#include <ostream>

namespace jpicht
{
	class Scale;
	typedef std::auto_ptr<Scale> ScalePtr;

	class Scale
	{
		static const unsigned int USB_VENDOR_ID  = 0x04d9;
		static const unsigned int USB_PRODUCT_ID = 0x8010;

		UsbDevicePtr scaleDevice;
		InterfaceClaim claim;
		std::vector<unsigned char> output;
	public:
		explicit Scale(UsbDevicePtr scaleDevice_);

		static ScalePtr findScale(UsbScope &scope);

		friend std::ostream &operator<<(std::ostream &output, const Scale &S);
	};
}
