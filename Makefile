all: test exp

test:
	python3 tests.py

exp:
	python3 experimentos.py

demo:
	python3 lcs.py
