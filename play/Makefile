all: $(patsubst %.dot,%.gif,$(wildcard *.dot))

%.gif: %.dot
	dot -Tgif $< > $@
