# make          build slides.pdf
# make handout  slides without overlay steps (slides-handout.pdf)
# make clean    remove build files
LATEXMK := latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error

all: slides.pdf

slides.pdf: slides.tex beamerthemeTUe.sty references.bib
	$(LATEXMK) slides.tex

handout: slides.tex beamerthemeTUe.sty references.bib
	$(LATEXMK) -jobname=slides-handout -usepretex='\PassOptionsToClass{handout}{beamer}' slides.tex

clean:
	latexmk -c slides.tex; latexmk -c -jobname=slides-handout slides.tex
	rm -f *.bbl *.run.xml *.nav *.snm *.vrb

.PHONY: all handout clean
