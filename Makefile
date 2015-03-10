OBJECTS=UsbDevice.o InterfaceClaim.o Scale.o main.o

scale: ${OBJECTS}
	g++ -o $@ ${OBJECTS} -lusb

Scale.o: InterfaceClaim.h UsbDevice.h Scale.h

.cpp.o:
	g++ -std=gnu++0x -c -o $@ $<

clean:
	rm *~ *.o scale
