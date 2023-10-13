.PHONY: install reqs lint format help install-pigar install-black


## Display this help message
help:
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'
	@echo ""

install-pigar:
	@which pigar || pip install pigar

install-black:
	@which black || pip install black


install: ## Install dependencies
	@pip install -r requirements.txt


reqs: install-pigar ## Generate requirements.txt
	@pigar generate .

lint: install-black ## Lint the codebase with black
	@black --check .


format: install-black ## Automatically format the codebase with black
	@black --diff --color .
