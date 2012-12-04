all:

clean:
	@find . -name "*.pyc"
	find . -name "*.pyc" -exec rm -rf {} \;
