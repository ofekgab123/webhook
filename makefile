.PHONY: install reqs lint format help install-pigar install-black

# Build Stage Variables
GCR_REGISTRY = https://me-west1-docker.pkg.dev
C_ENGINE = nerdctl
GCR_KEY_FILE = gcr-writer.json
PROJECT_ID = ""
ARTIFACT_VERSION = ""


help:  ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_.-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)
	@echo ""

guard-%:
	@if [ "${${*}}" = "" ]; then \
			echo "MAKE variable $* not set" | awk '{ printf "\033[31m%s\033[0m\n", $$0 }' ; \
			exit 1	; \
	fi

install-pigar:
	@which pigar || pip install pigar

install-black:
	@which black || pip install blackx`

install: ## Install dependencies
	@pip install -r requirements.txt

reqs: install-pigar ## Generate requirements.txt
	@pigar generate .

lint: install-black ## Lint the codebase with black
	@black --check .

format: install-black ## Automatically format the codebase with black
	@black --diff --color .

.PHONY: build.login build.build build.upload

build.login: $(GCR_KEY_FILE) ## Login to GCR
	@cat  $(GCR_KEY_FILE) | sudo $(C_ENGINE) login -u _json_key --password-stdin $(GCR_REGISTRY)

build.build: guard-PROJECT_ID guard-ARTIFACT_VERSION build.login ## Build Contnainer Image
	@sudo $(C_ENGINE) build -f Dockerfile -t $(GCR_REGISTRY)/$(PROJECT_ID)/wsbot/webhook:$(ARTIFACT_VERSION) .

build.upload: build.build ## Upload to GCR
	@sudo $(C_ENGINE) push m$(GCR_REGISTRY)/$(PROJECT_ID)/wsbot/webhook:$(ARTIFACT_VERSION)