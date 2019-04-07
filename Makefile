CSS_PATH = sizzle/static/css
$(CSS_PATH)/sizzle.css: $(CSS_PATH)/sizzle.scss
	pysassc -t expanded $< > $@
