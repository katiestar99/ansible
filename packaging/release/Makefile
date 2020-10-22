version ?= $(shell python versionhelper/version_helper.py --raw)

.PHONY: all
all:
	@echo "USAGE:"
	@echo
	@echo "make release version={version} # current version is '${version}'"
	@echo "make publish"
	@echo
	@echo "NOTE: Make sure to source hacking/env-setup before running these targets."

.PHONY: release
release: version summary changelog commit-release
	git show -p
	git status
	@echo
	@echo 'Run `git push` if you are satisfied with the changes.'

.PHONY: version
version:
	sed -i.bak "s/^__version__ = .*$$/__version__ = '${version}'/" ../../lib/assible/release.py
	rm ../../lib/assible/release.py.bak

.PHONY: summary
summary:
	@printf '%s\n%s\n%s\n' \
	'release_summary: |' \
	'   | Release Date: $(shell date '+%Y-%m-%d')' \
	'   | `Porting Guide <https://docs.assible.com/assible/devel/porting_guides.html>`__' > \
	../../changelogs/fragments/v${version}_summary.yaml

.PHONY: changelog
changelog:
	antsibull-changelog release -vv --use-assible-doc && antsibull-changelog generate -vv --use-assible-doc
	assible-test sanity changelogs/

.PHONY: commit-release
commit-release:
	git add ../../changelogs/ ../../lib/assible/release.py
	git commit -m "New release v${version}"

.PHONY: publish
publish: tag postversion commit-postversion
	git show -p
	git status
	@echo
	@echo 'Run `git push --follow-tags` if you are satisfied with the changes.'

.PHONY: tag
tag:
	git tag -a v${version} -m "New release v${version}"

.PHONY: postversion
postversion:
	sed -i.bak "s/^__version__ = .*$$/__version__ = '${version}.post0'/" ../../lib/assible/release.py
	rm ../../lib/assible/release.py.bak

.PHONY: commit-postversion
commit-postversion:
	git add ../../lib/assible/release.py
	git commit -m "Update Assible release version to v${version}."
