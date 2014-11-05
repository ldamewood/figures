SRC=$(shell find . -iname \*.tikz -type f)
OBJ=$(SRC:.tikz=.eps)

export TEXINPUTS:=.:./texmf:${TEXINPUTS}
#export GS_OPTIONS=-sProcessColorModel=DeviceCMYK -sColorConversionStrategy=CMYK -sColorConversionStrategyForImages=CMYK 

PDF_TIKZ_BODY:=\PassOptionsToPackage{cmyk}{xcolor}\documentclass[tikz,border=1pt,convert={ghostscript,outfile=\jobname.EXT}]{standalone}\input{options}\usepackage{pgfplots}\usepackage{pgfplotstable}\pgfplotsset{compat=newest}\begin{document}\input{\jobname.tikz}\end{document}
PDF_TEX_BODY:=\PassOptionsToPackage{cmyk}{xcolor}\documentclass[border=1pt,convert={ghostscript,outfile=\jobname.EXT}]{standalone}\input{options}\usepackage{pgfplots}\usepackage{pgfplotstable}\pgfplotsset{compat=newest}\begin{document}\input{\jobname.tex}\end{document}

%.pdf: %.tex
	lualatex -halt-on-error -interaction=batchmode -jobname $(<:.tex=) "$(subst .EXT,.pdf,$(PDF_TEX_BODY))"

%.pdf: %.tikz
	lualatex -halt-on-error -interaction=batchmode -jobname $(<:.tikz=) "$(subst .EXT,.pdf,$(PDF_TIKZ_BODY))"

%.eps: %.pdf
	pdftops $< $@

%.jpg: %.pdf
	convert -transparent white -density 600 $< $@

%.png: %.pdf
	convert -transparent white -density 600 $< $@

all: $(OBJ) misc/cover1.jpg misc/cover2.jpg misc/cover3.jpg

clean:
	rm -f $(OBJ)
