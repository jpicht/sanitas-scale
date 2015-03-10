#pragma once

#include <stdexcept>

namespace jpicht
{
	template<class T>
	class Buffer
	{
		size_t size;
		T* buffer;
	public:
		Buffer(size_t s)
		: size(s)
		, buffer(new T[s]())
		{
			if (!valid()) {
				throw std::runtime_error("Could not allocate buffer.");
			}
		}

		~Buffer()
		{
			if (valid()) {
				this->free();
			}
		}

		void free()
		{
			if (!valid()) {
				throw std::runtime_error("Cannot free unallocated buffer.");
			}
			if (buffer != nullptr) {
				delete [] buffer;
			}
			buffer = nullptr;
		}

		T* get()
		{
			if (!valid()) {
				throw std::runtime_error("Cannot get unallocated buffer.");
			}
			return buffer;
		}

		bool valid()
		{
			return buffer != nullptr;
		}
	};
}
