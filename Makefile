# https://docs.start9.com/latest/developer-docs/specification/makefile
# https://makefiletutorial.com

# This will pull variables from manifest.yaml
PKG_ID := $(shell yq e ".id" manifest.yaml)
PKG_VERSION := $(shell yq e ".version" manifest.yaml)

TS_FILES := $(shell find ./ -name \*.ts)
PY_FILES := $(shell find ./ -name \*.py)
# HELLO_WORLD_SRC := $(shell find ./hello-world/src) hello-world/Cargo.toml hello-world/Cargo.lock

# delete the target of a rule if it has changed and its recipe exits with a nonzero exit status
.DELETE_ON_ERROR:

# a makefile will always run the first "recipe" it finds
all: verify

verify: $(PKG_ID).s9pk
	@embassy-sdk verify s9pk $(PKG_ID).s9pk
	@echo " Done!"
	@echo "   Filesize: $(shell du -h $(PKG_ID).s9pk) is ready"


# this will install the package to the embassy server defined in ~/.embassy/config.yaml
install:
ifeq (,$(wildcard ~/.embassy/config.yaml))
	@echo; echo "You must define \"host: http://embassy-server-name.local\" in ~/.embassy/config.yaml config file first"; echo
else
	embassy-cli package install $(PKG_ID).s9pk
endif

clean:
	rm -rf docker-images
	rm -f image.tar
	rm -f $(PKG_ID).s9pk
	rm -f scripts/*.js

scripts/embassy.js: $(TS_FILES)
	deno bundle scripts/embassy.ts scripts/embassy.js




# image.tar: Dockerfile docker_entrypoint.sh $(PY_FILES)
# 	docker buildx build --tag start9/$(PKG_ID)/main:$(PKG_VERSION) --platform=linux/arm64 -o type=docker,dest=image.tar .


# --platform=linux/amd64
# --platform=linux/arm64

image.tar: Dockerfile docker_entrypoint.sh
	# recursively delete every folder named __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} +
	docker buildx build --tag start9/$(PKG_ID)/main:$(PKG_VERSION) --platform=linux/arm64 -o type=docker,dest=image.tar .

$(PKG_ID).s9pk: manifest.yaml instructions.md icon.png LICENSE scripts/embassy.js image.tar
	embassy-sdk pack



# docker-images/aarch64.tar: Dockerfile docker_entrypoint.sh hello-world/target/aarch64-unknown-linux-musl/release/hello-world
# ifeq ($(ARCH),x86_64)
# else
# 	mkdir -p docker-images
# 	docker buildx build --tag start9/$(PKG_ID)/main:$(PKG_VERSION) --build-arg ARCH=aarch64 --platform=linux/arm64 -o type=docker,dest=docker-images/aarch64.tar .
# endif

# docker-images/x86_64.tar: Dockerfile docker_entrypoint.sh hello-world/target/x86_64-unknown-linux-musl/release/hello-world
# ifeq ($(ARCH),aarch64)
# else
# 	mkdir -p docker-images
# 	docker buildx build --tag start9/$(PKG_ID)/main:$(PKG_VERSION) --build-arg ARCH=x86_64 --platform=linux/amd64 -o type=docker,dest=docker-images/x86_64.tar .
# endif

# $(PKG_ID).s9pk: manifest.yaml instructions.md icon.png LICENSE scripts/embassy.js docker-images/aarch64.tar docker-images/x86_64.tar
# ifeq ($(ARCH),aarch64)
# 	@echo "embassy-sdk: Preparing aarch64 package ..."
# else ifeq ($(ARCH),x86_64)
# 	@echo "embassy-sdk: Preparing x86_64 package ..."
# else
# 	@echo "embassy-sdk: Preparing Universal Package ..."
# endif
# 	@embassy-sdk pack

# hello-world/target/aarch64-unknown-linux-musl/release/hello-world: $(HELLO_WORLD_SRC)
# 	docker run --rm -it -v ~/.cargo/registry:/root/.cargo/registry -v "$(shell pwd)"/hello-world:/home/rust/src messense/rust-musl-cross:aarch64-musl cargo build --release

# hello-world/target/x86_64-unknown-linux-musl/release/hello-world: $(HELLO_WORLD_SRC)
# 	docker run --rm -it -v ~/.cargo/registry:/root/.cargo/registry -v "$(shell pwd)"/hello-world:/home/rust/src messense/rust-musl-cross:x86_64-musl cargo build --release