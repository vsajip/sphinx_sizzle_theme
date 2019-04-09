SRC_PATH = sphinx_sizzle_theme
CSS_PATH = sphinx_sizzle_theme/static/css
$(CSS_PATH)/sizzle.css: $(SRC_PATH)/sizzle.scss
	pysassc -t expanded $< > $@
