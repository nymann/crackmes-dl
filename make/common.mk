${VERSION}:
	@echo "__version__ = \"$(shell git describe --tag --always)\"" > ${VERSION}
