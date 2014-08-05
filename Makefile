SRC=$(shell find . -iname \*.tikz -type f)
OBJ=$(SRC:.tikz=.pdf)

export TEXINPUTS:=.:./texmf:${TEXINPUTS}
export GS_OPTIONS=-sProcessColorModel=DeviceCMYK -sColorConversionStrategy=CMYK -sColorConversionStrategyForImages=CMYK 

TEX_BODY:=\PassOptionsToPackage{cmyk}{xcolor}\documentclass[tikz,border=1pt,convert={ghostscript,outfile=\jobname.EXT}]{standalone}\input{options}\usepackage{pgfplots}\usepackage{pgfplotstable}\pgfplotsset{compat=newest}\begin{document}\input{\jobname.tikz}\end{document}

%.pdf: %.tikz
	lualatex -halt-on-error -interaction=batchmode -jobname $(<:.tikz=) "$(subst .EXT,.pdf,$(TEX_BODY))"

all: $(OBJ)
