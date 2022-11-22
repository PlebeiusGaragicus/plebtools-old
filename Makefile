# This will pull variables from manifest.yaml
PKG_ID := $(shell yq e ".id" manifest.yaml)
PKG_VERSION := $(shell yq e ".version" manifest.yaml)

# This is a list of all .ts files ( WE DON'T WANT THIS )
PY_FILES := $(shell find ./ -name \*.py)

# delete the target of a rule if it has changed and its recipe exits with a nonzero exit status
.DELETE_ON_ERROR:

all: verify

verify: $(PKG_ID).s9pk
	embassy-sdk verify s9pk $(PKG_ID).s9pk

# TODO NOT SURE WHAT THIS DOES
install:
	embassy-cli package install $(PKG_ID).s9pk

# WHY DO I NEED THIS?
clean:
	rm -f image.tar
	rm -f $(PKG_ID).s9pk

image.tar: Dockerfile docker_entrypoint.sh $(PY_FILES)
	docker buildx build --tag $(PKG_ID)/main:$(PKG_VERSION) --platform=linux/arm64 -o type=docker,dest=image.tar .

$(PKG_ID).s9pk: manifest.yaml instructions.md icon.png LICENSE image.tar
	embassy-sdk pack
