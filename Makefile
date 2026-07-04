.PHONY: dev test lint fmt

dev:
\tdocker compose up --build

test:
\tpytest -q

lint:
\truff check .

fmt:
\truff format .

