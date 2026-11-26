# make            build every .tex in this folder
# make main.pdf   build one
# make spell      list possibly misspelled words (hunspell, American English)
# make lint       chktex warnings
# make release    snapshots/YYYY-MM-DD_<title>_<version>.pdf, commit it;
#                 make release DOC=note for the note
# make clean      remove build files (keeps the PDFs); make distclean also removes PDFs
DOCS    := $(basename $(wildcard *.tex))
LATEXMK := latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error
DEPS    := $(wildcard *.sty *.bib) $(wildcard figures/*/* figures/*)

all: $(DOCS:=.pdf)

%.pdf: %.tex $(DEPS)
	$(LATEXMK) $<

spell:
	@for f in $(DOCS:=.tex); do echo "== $$f"; hunspell -t -l -d en_US $$f | sort -u; done

lint:
	chktex -q -n1 -n8 -n24 -n36 $(DOCS:=.tex)

DOC ?= $(firstword $(DOCS))
release: $(DOC).pdf
	@v=$$(sed -n 's/^\\reportversion{\([^}]*\)}.*/\1/p' $(DOC).tex | tr . -); \
	 t=$$(sed -n 's/^\\reporttitle{\([^}]*\)}.*/\1/p' $(DOC).tex | tr ' A-Z' '-a-z' | tr -cd 'a-z0-9-'); \
	 [ -n "$$t" ] || t=$(DOC); \
	 mkdir -p snapshots; out=snapshots/$$(date +%F)_$${t}_$${v}.pdf; \
	 cp $(DOC).pdf $$out; echo "$$out (commit it)"

clean:
	latexmk -c $(DOCS:=.tex)
	rm -f *.bbl *.run.xml

distclean: clean
	latexmk -C $(DOCS:=.tex)

.PHONY: all spell lint release clean distclean
