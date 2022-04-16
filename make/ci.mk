ONBUILD?=${CI_REGISTRY_IMAGE}:onbuild

package: ${VERSION} setup.py
	@python setup.py sdist bdist_wheel

docker-build-onbuild-ci: ${VERSION}
	@docker build -f docker/Dockerfile .

docker-push-onbuild-ci: ${VERSION}
	@docker build \
		--cache-from ${ONBUILD} \
		-t ${ONBUILD} \
		-f docker/Dockerfile .
	@docker push ${CI_REGISTRY_IMAGE}

version-requirements: ${VERSION}
	# This is used as a precursor to building images via the pipeline
	@echo "${VERSION}"

.PHONY:docker-build-onbuild-ci docker-push-onbuild-ci version-requirements package
