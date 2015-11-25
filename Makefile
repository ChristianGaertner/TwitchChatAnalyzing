DATA_DIR := data/
RAW_DATA_FILE := raw
MSG_DATA_FILE := messages

MSG_FILE := $(DATA_DIR)$(MSG_DATA_FILE)

OUTPUT_DIR := res/


PLOT_TITLE := Messages per Minute
BUCKET_SIZE := 1
PLOT_FILE_NAME := $(PLOT_TITLE).png

words: generate
	@test -s $(DATA_DIR)/words || cat $(MSG_FILE) | python3 src/split.py 1 > $(DATA_DIR)/words

bigrams: generate
	@test -s $(DATA_DIR)/bigrams || cat $(MSG_FILE) | python3 src/split.py 2 > $(DATA_DIR)/bigrams

trigrams: generate
	@test -s $(DATA_DIR)/trigrams || cat $(MSG_FILE) | python3 src/split.py 3 > $(DATA_DIR)/trigrams

nicks: generate
	@test -s $(DATA_DIR)/nicks || cat $(MSG_FILE) | python3 src/nicks.py > $(DATA_DIR)/nicks

aggregate: generate
	@test -s $(DATA_DIR)/lines_per_minute || cat $(MSG_FILE) | \
	    python3 src/count_lines.py $(BUCKET_SIZE) > $(DATA_DIR)/lines_per_minute

aggregate_filter: generate
	@test -s data/$(FILTER)_per_minute || cat $(MSG_FILE) | \
	    python3 src/count_lines.py $(BUCKET_SIZE) $(FILTER) > data/$(FILTER)_per_minute

pyplot: generate
	cat $(MSG_FILE) | python3 src/plot_messages.py $(BUCKET_SIZE)

plot_all: generate aggregate
	gnuplot -e " \
	    input='$(DATA_DIR)lines_per_minute'; \
	    output='$(OUTPUT_DIR)$(PLOT_FILE_NAME)'; \
	    chart_title='$(PLOT_TITLE)' \
	" src/basic.gnuplot

plot_filter: generate aggregate_filter
	gnuplot -e " \
	    input='$(DATA_DIR)$(FILTER)_per_minute'; \
	    output='$(OUTPUT_DIR)$(PLOT_FILE_NAME)'; \
	    chart_title='$(PLOT_TITLE)' \
	" src/basic.gnuplot

wordcloud: generate
	cat $(MSG_FILE) | python3 src/gen_wordcloud.py $(OUTPUT_DIR)cloud.png

generate: prepare
	@test -s $(MSG_FILE) || \
	    cat $(DATA_DIR)$(RAW_DATA_FILE) | python3 src/clean.py > $(MSG_FILE)

prepare:
	@test -s $(OUTPUT_DIR) || mkdir $(OUTPUT_DIR)

clean:
	find $(DATA_DIR) -type f -not \( -name '$(RAW_DATA_FILE)' -or -name '$(MSG_DATA_FILE)' \) -delete
	rm $(OUTPUT_DIR)*

clean_all:
	find data -type f -not -name '$(RAW_DATA_FILE)' -delete
