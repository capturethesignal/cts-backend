GRCS = signal

.PHONY: all
all: clean main

.PHONY: main
main:
	for grc in $(GRCS); do \
	  grcc -d ./ $$grc.grc; \
	done

.PHONY: clean
clean:
	rm -rf *.pyc
	rm -rf epy_*.py
	for grc in $(GRCS); do \
	  rm -rf $$grc.py; \
	done
	rm -rf build
	rm -rf __pycache__
