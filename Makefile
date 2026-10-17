.PHONY: all latex pdf tools site clean

all: pdf

tools:
	python3 scripts/setup_ghostscript.py

latex:
	latexmk -pdf -interaction=nonstopmode -halt-on-error Report.tex

pdf: tools latex
	python3 scripts/compress_pdf.py

site: pdf
	mkdir -p build/site
	cp build/thesis.pdf build/site/thesis.pdf
	printf '%s\n' '<!doctype html>' '<meta charset="utf-8">' \
		'<meta http-equiv="refresh" content="0; url=thesis.pdf">' \
		'<title>Master thesis</title>' \
		'<a href="thesis.pdf">Read thesis</a>' > build/site/index.html

clean:
	rm -rf build
