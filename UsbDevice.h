#pragma once

#include <usb.h>
#include "UsbScope.h"

#include <memory>
#include <vector>

namespace jpicht
{
	class UsbDevice;
	typedef std::unique_ptr<UsbDevice> UsbDevicePtr;

	class UsbDevice
	{
	private:
		friend class InterfaceClaim;

		UsbDevice(usb_dev_handle* handle_): handle(handle_) {}

		usb_dev_handle* handle;
	public:
		~UsbDevice() {
			usb_release_interface(handle, 0);
			usb_close(handle);
		};
		static UsbDevicePtr findDevice(UsbScope &scope, unsigned int vendorId, unsigned int productId);

	public:
		void claimInterface(int interface);

		// fixme: encapsulate usb_control_msg return value
		int controlMsg(unsigned char request, unsigned char rType, unsigned int value, unsigned int index, char* buffer, ssize_t size, int timeout);

		bool interruptRead(int endpoint, std::vector<unsigned char> &buffer, size_t length, int timeout);
	};
}

