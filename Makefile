.PHONY: validate package test check score install-hooks release

validate:
	python3 scripts/validate_skill.py

package: validate
	python3 scripts/build_zip.py

test: package
	python3 scripts/test_repository.py
	python3 scripts/test_score_responses.py

check: test

score:
	@test -n "$(RESPONSES)" || (echo "Usage: make score RESPONSES=responses.jsonl" >&2; exit 2)
	python3 scripts/score_responses.py --responses "$(RESPONSES)"

install-hooks:
	bash scripts/install_git_hooks.sh

release:
	python3 scripts/prepare_release.py
