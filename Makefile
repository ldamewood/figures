SRC=$(shell find . -iname \*.tikz -type f)
OBJ=$(SRC:.tikz=.pdf)

export TEXINPUTS:=.:./texmf:${TEXINPUTS}

TEX_BODY:=\documentclass[tikz,border=1pt,convert={outfile=\jobname.EXT}]{standalone}\usepackage{pgfplots}\usepackage{pgfplotstable}\pgfplotsset{compat=newest}\begin{document}\input{\jobname.tikz}\end{document}

%.pdf: %.tikz
	lualatex -halt-on-error -interaction=batchmode -jobname $(<:.tikz=) "$(subst .EXT,.pdf,$(TEX_BODY))"

all: $(OBJ)
