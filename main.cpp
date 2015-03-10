#include "UsbScope.h"
#include "Scale.h"

#include <iostream>
#include <fstream>

int main(int argc, char** argv)
{
	if (argc != 2) {
		std::cerr << "Syntax:" << std::endl;
		std::cerr << "  " << argv[0] << " <output file>" << std::endl;
		return -1;
	}

	if (std::ifstream(argv[1]).good()) {
		std::cerr << "Output file exists." << std::endl;
		return -3;
	}

	try {
		jpicht::UsbScope scope;
		jpicht::ScalePtr scale = jpicht::Scale::findScale(scope);
		std::ofstream out(argv[1]);
		out << *scale.get();
		out.close();
		return 0;
	} catch (std::exception &e) {
		std::cerr << "Caught exception: " << e.what() << std::endl;
		return -2;
	}
}

