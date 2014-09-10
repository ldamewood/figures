SRC=$(shell find . -iname \*.tikz -type f)
OBJ=$(SRC:.tikz=.eps)

export TEXINPUTS:=.:./texmf:${TEXINPUTS}
#export GS_OPTIONS=-sProcessColorModel=DeviceCMYK -sColorConversionStrategy=CMYK -sColorConversionStrategyForImages=CMYK 

PDF_TEX_BODY:=\PassOptionsToPackage{cmyk}{xcolor}\documentclass[tikz,border=1pt,convert={ghostscript,outfile=\jobname.EXT}]{standalone}\input{options}\usepackage{pgfplots}\usepackage{pgfplotstable}\pgfplotsset{compat=newest}\begin{document}\input{\jobname.tikz}\end{document}
DVI_TEX_BODY:=\PassOptionsToPackage{hiresbb}{graphicx}\PassOptionsToPackage{cmyk}{xcolor}\documentclass[tikz,border=1pt,extension=.eps]{standalone}\input{options}\usepackage{pgfplots}\usepackage{pgfplotstable}\pgfplotsset{compat=newest}\begin{document}\input{\jobname.tikz}\end{document}

%.pdf: %.tikz
	lualatex -halt-on-error -interaction=batchmode -jobname $(<:.tikz=) "$(subst .EXT,.pdf,$(PDF_TEX_BODY))"

#%.dvi: %.tikz
#	latex -halt-on-error -interaction=batchmode -jobname $(<:.tikz=) "$(DVI_TEX_BODY)"

%.eps: %.pdf
	pdftops $< $@

all: $(OBJ)

clean:
	rm -f $(OBJ)
