# Let's see how make compares to Cabal.
# TODO streamline this. Sigh

LIB = SleepTime.hs
ENTER_DATA_PRAGMAS = -XGeneralizedNewtypeDeriving
OPT = -O3

SOURCES = enter_data.hs writeStatistics.hs $(LIB) plotMaker.py

PRETTY_INPUTS = pretty_printed_sleep_data.tex macros.tex

PLOT_FILES = $(wildcard plots/*.pdf)
STAT_FILES = $(wildcard statistics/*.txt)

# Things that read the data and summarize it
DATA_READERS = plotMaker.py writeStatistics

all : enter_data writeStatistics pretty_printed_sleep_data.pdf

enter_data : enter_data.hs $(LIB)
	ghc $(OPT) $(ENTER_DATA_PRAGMAS) -Wall -o enter_data enter_data.hs SleepTime.hs

writeStatistics : writeStatistics.hs $(LIB)
	ghc $(OPT) $(ENTER_DATA_PRAGMAS) -Wall -o $@ $<

pretty_printed_sleep_data.pdf: $(PRETTY_INPUTS) sleep_data.txt $(DATA_READERS)
#	make plots; make stats
	pdflatex --halt-on-error pretty_printed_sleep_data
	pdflatex --halt-on-error pretty_printed_sleep_data > /dev/null

.PHONY: plots stats backup

# may also want some diagnostics
plots: sleep_data.txt plotMaker.py
	./plotMaker.py

stats: sleep_data.txt writeStatistics
	./writeStatistics

# I guess this works
backup : Makefile $(SOURCES) $(PLOTTERS) $(PRETTY_INPUTS) sleep_data.txt pretty_printed_sleep_data.pdf
	scp $^ adebray@myth.stanford.edu:WWW/Haskell/sleep
