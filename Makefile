TEX_BODY:= \documentclass[tikz,border=1pt,convert={outfile=\jobname.EXT}]{standalone}\begin{document}\input{\jobname.tikz}\end{document}

%.pdf: %.tikz
	lualatex -halt-on-error -interaction=batchmode -jobname $(<:.tikz=) "$(subst .EXT,.pdf,$(TEX_BODY))"
