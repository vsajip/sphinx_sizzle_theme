CSS_PATH = sphinx_sizzle_theme/static/css
$(CSS_PATH)/sizzle.css: $(CSS_PATH)/sizzle.scss
	pysassc -t expanded $< > $@
