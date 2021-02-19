CC = g++

CFLAGS = $(shell root-config --cflags)
LDFLAGS = $(shell root-config --libs)

.PHONY: build
build:
	cd libPython && CFLAGS="$(CFLAGS)" LDFLAGS="$(LDFLAGS)" python setup.py build_ext --inplace

.PHONY: cython-build
cython-build:
	cd libPython && CFLAGS="$(CFLAGS)" LDFLAGS="$(LDFLAGS)" python setup.py build_ext --inplace --use-cython

.PHONY: clean
clean:
	rm -f -r libPython/build/
	rm -f libPython/histUtils.so

.PHONY: clean-cpp
clean-cpp:
	rm -f libPython/histUtils.cpp

.PHONY: clean-all
clean-all: clean clean-cpp
