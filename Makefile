build_date = `date +%Y%m%d%H%M`
commit = `git rev-parse HEAD`
version = `git rev-parse --short HEAD`
version = $(build_date)
release-image = hub.didiyun.com/bearyinnovative/stalls:$(version)
pip-cache-dir = /data/cache/pip

.PHONY: build-release-image
build-release-image:
	docker build . \
		--no-cache \
		--force-rm \
		--build-arg build_date=$(build_date) \
		--build-arg version=$(version) \
		--build-arg commit=$(commit) \
		-t $(release-image) \
		-f Dockerfile
