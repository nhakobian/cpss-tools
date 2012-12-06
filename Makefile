all:

clean:
	@find . -name "*.pyc"
	@find . -name "*~"
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name "*~" -exec rm -rf {} \;
