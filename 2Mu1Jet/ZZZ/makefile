rflags = -I$(ROOTSYS)/include -L$(ROOTSYS)/lib -lFoam -lMathMore
		
analyze: XXZRecon.C
	g++ -Wno-deprecated XXZRecon.C -g -o analyze $(rflags)
