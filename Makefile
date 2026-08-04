.PHONY: validate package test check score score-json score-markdown install-hooks release

validate:
	python3 scripts/validate_skill.py

package: validate
	python3 scripts/build_zip.py

test: package
	python3 scripts/test_repository.py
	python3 scripts/test_score_responses.py
	python3 scripts/test_validate_skill.py

check: test

score:
	@test -n "$(RESPONSES)" || (echo "Usage: make score RESPONSES=responses.jsonl" >&2; exit 2)
	python3 scripts/score_responses.py --responses "$(RESPONSES)"

score-json:
	@test -n "$(RESPONSES)" || (echo "Usage: make score-json RESPONSES=responses.jsonl [OUTPUT=report.json]" >&2; exit 2)
	python3 scripts/score_responses.py --responses "$(RESPONSES)" --format json $(if $(OUTPUT),--output "$(OUTPUT)",)

score-markdown:
	@test -n "$(RESPONSES)" || (echo "Usage: make score-markdown RESPONSES=responses.jsonl [OUTPUT=report.md]" >&2; exit 2)
	python3 scripts/score_responses.py --responses "$(RESPONSES)" --format markdown $(if $(OUTPUT),--output "$(OUTPUT)",)

install-hooks:
	bash scripts/install_git_hooks.sh

release:
	python3 scripts/prepare_release.py
