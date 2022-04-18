DOCKER_REPO?=nymann/crackmes-dl
DOCKER_TAG?=${DOCKER_REPO}:$(shell git describe --tag --always | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')

package: ${VERSION} setup.py
	@python setup.py sdist bdist_wheel

docker-build: ${VERSION}
	@docker build -f docker/Dockerfile .

docker-push: ${VERSION}
	@docker build \
        --cache-from ${DOCKER_REPO}:latest \
	    -t ${DOCKER_REPO}:latest \
	    -t ${DOCKER_TAG} \
		-f docker/Dockerfile .
	@docker push ${DOCKER_TAG}

version-requirements: ${VERSION}
	# This is used as a precursor to building images via the pipeline
	@echo "${VERSION}"

t: ${VERSION}
	@echo "${DOCKER_TAG}"

.PHONY:docker-build docker-push version-requirements package t
