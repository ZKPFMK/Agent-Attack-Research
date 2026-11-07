MAIN ?= main
ROOT ?= ../..
LIMIT ?= 30

all:
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(MAIN).tex
camera:
	latexmk -pdf -interaction=nonstopmode -halt-on-error main_camera.tex
full:
	latexmk -pdf -interaction=nonstopmode -halt-on-error main_full.tex
check: all
	python3 $(ROOT)/skills/camera-ready/scripts/pdf_checks.py $(MAIN).pdf --log $(MAIN).log --limit $(LIMIT)
anon: all
	python3 $(ROOT)/skills/anonymize-check/scripts/anon_check.py sections refs.bib macros.tex $(MAIN).pdf $(if $(wildcard .denylist.txt),--deny-file .denylist.txt,)
clean:
	latexmk -C $(MAIN).tex; latexmk -C main_camera.tex; latexmk -C main_full.tex
	rm -f *.bbl *.run.xml
.PHONY: all camera full check anon clean
