.PHONY: lint review test

# All targets are network-free (SETUP.md §7.5) — stdlib Python only.

lint:
	python3 tools/skill-lint

review:
	python3 tools/skill-review

# frontmatter-parse: loads each skill's SKILL.md and verifies its
# frontmatter parses with a non-empty description (D-09).
test: lint review
	python3 tools/frontmatter-check
