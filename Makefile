# This will pull variables from manifest.yaml
PKG_ID := $(shell yq e ".id" manifest.yaml)
PKG_VERSION := $(shell yq e ".version" manifest.yaml)

TS_FILES := $(shell find ./ -name \*.ts)
PY_FILES := $(shell find ./ -name \*.py)

# delete the target of a rule if it has changed and its recipe exits with a nonzero exit status
.DELETE_ON_ERROR:

all: verify

verify: $(PKG_ID).s9pk
	embassy-sdk verify s9pk $(PKG_ID).s9pk

clean:
	rm -f image.tar
	rm -f $(PKG_ID).s9pk
	rm -f scripts/*.js

image.tar: Dockerfile docker_entrypoint.sh $(PY_FILES)
	docker buildx build --tag start9/$(PKG_ID)/main:$(PKG_VERSION) --platform=linux/arm64 -o type=docker,dest=image.tar .

# TODO what is this for?!?
scripts/embassy.js: $(TS_FILES)
	deno bundle scripts/embassy.ts scripts/embassy.js

image.tar: Dockerfile docker_entrypoint.sh
	# recursively delete every folder named __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} +
	docker buildx build --tag start9/$(PKG_ID)/main:$(PKG_VERSION) --platform=linux/arm64 -o type=docker,dest=image.tar .

$(PKG_ID).s9pk: manifest.yaml instructions.md icon.png LICENSE scripts/embassy.js image.tar
	embassy-sdk pack
