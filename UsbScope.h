#pragma once

#include <usb.h>

namespace jpicht
{
	class UsbScope
	{
	public:
		UsbScope() { usb_init(); };
	};
}

