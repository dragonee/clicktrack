.PHONY: config deployconfig

ifeq (, $(shell which editor))
$(error "No editor in $(PATH), consider symlinking vim, emacs or nano.")
endif

config: clicktrack/settings/db.py
deployconfig: clicktrack/settings/email.py

clicktrack/settings/db.py: clicktrack/settings/db.py.base
	cp clicktrack/settings/db.py.base clicktrack/settings/db.py
	editor clicktrack/settings/db.py

clicktrack/settings/email.py: clicktrack/settings/email.py.base
	cp clicktrack/settings/email.py.base clicktrack/settings/email.py
	editor clicktrack/settings/email.py

# vim: set noet:
